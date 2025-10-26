use serde::{Serialize, Deserialize};
use jsonwebtoken::{encode, Header, EncodingKey};
use std::{env, fs, process};

#[derive(Debug, Serialize, Deserialize)]
struct Claims {
    sub: String,
    role: String,
}

fn main() {
    // Load environment variables
    let jwt_secret = env::var("JWT_SECRET")
        .expect("JWT_SECRET environment variable not set");

    let service_name = env::var("SERVICE_NAME")
        .expect("SERVICE_NAME environment variable not set");

    let output_path = env::var("OUTPUT_PATH")
        .expect("OUTPUT_PATH environment variable not set");


    let my_claims = Claims {
        sub: service_name,
        role: "service".to_string(),
    };

    let token = encode(
        &Header::default(),
        &my_claims,
        &EncodingKey::from_secret(jwt_secret.as_bytes()),
    )
    .expect("Failed to encode JWT");


    fs::write(&output_path, &token).expect("Failed to write token to file");
    println!("JWT successfully written to {}", output_path);
}
