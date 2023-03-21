pub mod types;

use std::env;

use rand::prelude::*;
use serde_json::json;
use actix_web::{HttpServer, HttpResponse, App, get, post, web, Responder, Result};
use deadpool_redis::{redis::cmd, Config, Runtime, CreatePoolError};

use types::SimInput;

const REDIS_JOBS_QUEUE: &'static str = "jobs";

fn redis_new() -> Result<deadpool_redis::Pool, CreatePoolError> {
    let url = env::var("REDIS").expect("Required: Broker redis url");
    let cfg = Config::from_url(url);
    let runtime = Some(Runtime::Tokio1);

    cfg.create_pool(runtime)
}

#[post("/load")]
async fn load() -> impl Responder {
    "Broker load route."
}

#[post("/run")]
async fn run(pool: web::Data<deadpool_redis::Pool>, json: web::Json<SimInput>) -> impl Responder {
    println!("{:?}", json);
    let mut conn = pool.get().await.unwrap();
    let job_id = {
        let mut rng = rand::thread_rng();
        rng.gen::<u64>()
    };
    let res = json!({"jobID":job_id});
    let db_entry = serde_json::to_string(&json).unwrap();

    match cmd("SET")
        .arg(&[REDIS_JOBS_QUEUE, &db_entry])
        .query_async::<_, ()>(&mut conn)
        .await {
            Ok(_) => HttpResponse::Ok().body(res.to_string()),
            Err(_) => HttpResponse::BadRequest().body("Unable to enqueue job."),
        }
}

#[get("/")]
async fn index() -> impl Responder {
    "Broker index route."
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    
    let host = env::var("HOST")
        .expect("Required: Broker server host.");

    let port = env::var("PORT")
        .expect("Required: Broker server port.")
        .parse::<u16>()
        .expect("Required: Broker server port must be u16.");

    // TODO: Actix middleware logging.
    env::set_var("RUST_LOG", "debug");
    env_logger::init();

    let pool = web::Data::new(redis_new().unwrap());
    HttpServer::new(move || {
        App::new()
            .app_data(pool.clone())
            .service(index)
            .service(run)
            .service(load)
    })
    .bind((host, port))?
    .run()
    .await
}
