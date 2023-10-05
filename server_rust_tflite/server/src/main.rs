use rocket::{self, Orbit, Rocket, State};
use rocket::serde::json::{json, Json, Value};
use rocket::serde::{Deserialize, Serialize};
use rocket::fairing::{Fairing, Info, Kind};
use std::str::FromStr;
use std::sync::{Arc, Mutex};
use std::time::{Instant, SystemTime, UNIX_EPOCH};
use tflitec::interpreter::Interpreter;

struct ThreadSafeInterpreter {
    mutexed_interpreted: Arc<Mutex<Interpreter>>,
}

#[derive(Debug, Deserialize, Serialize)]
#[serde(crate = "rocket::serde")]
pub struct MyData {
    image_array: Vec<Vec<Vec<f32>>>,
}

fn flatten(input: Vec<Vec<Vec<f32>>>) -> Vec<f32> {
    input
        .into_iter()
        .flat_map(|inner_vec| inner_vec.into_iter())
        .flat_map(|inner_vec| inner_vec.into_iter())
        .collect()
}


fn get_current_time() -> u128 {
    let start = SystemTime::now();
    let since_the_epoch = start
        .duration_since(UNIX_EPOCH)
        .expect("Time went backwards");
    since_the_epoch.as_nanos()
}

fn call_interpreter(
    interpreter: std::sync::MutexGuard<'_, Interpreter>,
    input_value: &Vec<f32>,
) -> Vec<f32> {
    let input_tensor = interpreter.input(0).unwrap();
    _ = input_tensor.set_data(input_value);
    _ = interpreter.invoke();
    let output_tensor = interpreter.output(0).unwrap();
    let output_vector = output_tensor.data::<f32>().to_vec();
    output_vector
}


#[derive(Default, Clone)]
struct LiftOffTimer {}

#[rocket::async_trait]
impl Fairing for LiftOffTimer {
    fn info(&self) -> Info {
        Info {
            name: "GET/POST Counter",
            kind: Kind::Liftoff,
        }
    }

    async fn on_liftoff(&self, _rocket: &Rocket<Orbit>) {
        let now = get_current_time();
        let start_time = std::env::var("START_TIME").unwrap();
        let start_time_nanos = u128::from_str(&start_time).unwrap();
        println!(
            "**** Booting took {:?} ms",
            (now - start_time_nanos) as f32 / 1000000.0
        );
    }
}

#[rocket::post("/", format = "json", data = "<payload>")]
async fn hello(
    payload: Json<MyData>,
    threadsafe_interpreter: &State<ThreadSafeInterpreter>,
) -> Value {
    let rgb_vec = &payload.image_array;
    let rgb_vec = flatten(rgb_vec.to_owned());
    let interpreter = threadsafe_interpreter.mutexed_interpreted.lock().unwrap();
    let now: Instant = Instant::now();
    let output_vector = call_interpreter(interpreter, &rgb_vec);
    let elapsed = now.elapsed();
    println!("**** Inference took: {:?}", elapsed);
    json!({"output_vector": output_vector})
}

#[rocket::launch]
fn launch_function() -> _ {
    let now = Instant::now();
    let interpreter = Interpreter::with_model_path("model.tflite", None).unwrap();
    _ = interpreter.allocate_tensors();
    println!(
        "**** Loading Model {:?} ms",
        (now.elapsed().as_nanos() as f32) / 1000000.0
    );
    let threadsafe_interpreter = ThreadSafeInterpreter {
        mutexed_interpreted: Arc::new(Mutex::new(interpreter)),
    };

    rocket::build()
        .mount("/predict", rocket::routes![hello])
        .manage(threadsafe_interpreter)
        .attach(LiftOffTimer::default())
}
