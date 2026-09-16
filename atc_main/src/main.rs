use macroquad::prelude::*;
use trig::Trig;

mod camera;
use camera::Camera;

fn draw_centered_text(text: &str, center_x: f32, center_y: f32, font_size: f32, color: Color) {
    let text_dims = measure_text(text, None, font_size as u16, 1.0);

    // minus half-width for horizontal center
    let x = center_x - text_dims.width / 2.0;
    let y = center_y + text_dims.height / 2.0;

    // draw_text (text, x, y, font_size, colour)
    // where x, y is bottom-left baseline anchor
    draw_text(text, x, y, font_size, color);
}

fn deg_to_coord(radius: f64, degrees: f64) -> (f64, f64) {
    // Given SOH CAH TOA
    // x = cos(degrees) * radius
    // y = sin(degrees) * radius
    (
        degrees.to_radians().cos() * radius,
        degrees.to_radians().sin() * radius,
    )
}

#[macroquad::main("AtcMain")]
async fn main() {
    // Default camera parameters, assuming spherical-style camera.
    let cam_default_radius = 88.0;
    let cam_default_angle_elevation = 35.0;
    let cam_default_angle_rotation = 0.0;
    let cam_default_rotation_dps = 2.0;

    let mut cam_radius = cam_default_radius;
    let mut cam_angle_elevation = cam_default_angle_elevation;
    let mut cam_angle_rotation = cam_default_angle_rotation;
    let mut cam_target_xz = vec2(0.0, 0.0); // point camera is looking at on the ground plane
    let mut auto_rotate = true;

    loop {
        clear_background(LIGHTGRAY);

        // Mouse interaction
        let wheel = mouse_wheel();
        if wheel.1 != 0.0 {
            auto_rotate = false;
            cam_radius = (cam_radius - wheel.1 * 5.0).clamp(20.0, 300.0); // set min/max distance
            // with clamp
        }
        if is_mouse_button_down(MouseButton::Left) {
            let delta = mouse_delta_position();
            if delta.length_squared() > 0.0 {
                auto_rotate = false;
                let ctrl_pressed =
                    is_key_down(KeyCode::LeftControl) || is_key_down(KeyCode::RightControl);
                if ctrl_pressed {
                    cam_angle_rotation -= delta.x * 100.0;
                    cam_angle_elevation = (cam_angle_elevation + delta.y * 100.0).clamp(5.0, 85.0);
                } else {
                    let rad = cam_angle_rotation.to_radians();
                    let right = vec2(-rad.sin(), rad.cos());
                    let forward = vec2(-rad.cos(), -rad.sin());
                    let pan_speed = 0.25;
                    cam_target_xz -= (right * delta.x + forward * delta.y) * pan_speed;
                }
            }
        }

        // auto rotation
        if auto_rotate {
            cam_angle_rotation += cam_default_rotation_dps * get_frame_time();
        }

        // slices (number of lines)
        // spacing (how far apart)
        draw_grid(100, 1.0, BLACK, GRAY);

        next_frame().await;
    }
}

// Commenting out the old main for now

// #[macroquad::main("AtcMain")]
// async fn main() {
//     let mut mousepos: (f32, f32) = (0.0, 0.0);
//     let mut mouseclick: bool = false;
//     loop {
//         // runs everytime to clear the background
//         clear_background(GRAY);
//
//         // runs everytime in case the screen has been resized. Tracks the "center" of the screen
//         // screen (0,0) is the top left corner
//         let screen_center_x = screen_width() / 2.0; // +x is to the right
//         let screen_center_y = screen_height() / 2.0; // +y is down
//
//         let greeting = "Goofy Goomba";
//         let font_size = 32.0;
//         draw_centered_text(greeting, screen_center_x, screen_center_y, font_size, WHITE);
//         // draw_line(x1, y1, x1, y2, thickness, colour);
//         draw_line(0.0, 0.0, 100.0, 100.0, 10.0, BLUE);
//         draw_rectangle(screen_width() / 2.0 - 60.0, 100.0, 12.0, 60.0, GREEN);
//
//         if is_mouse_button_pressed(MouseButton::Left) {
//             mouseclick = true;
//
//             // TODO: determine how to map screen position to "reference" position
//             mousepos = mouse_position();
//
//             // TODO: spawn plane
//         }
//         if (mouseclick) {
//             draw_circle(mousepos.0, mousepos.1, 25.0, RED);
//         }
//
//         next_frame().await
//     }
// }
