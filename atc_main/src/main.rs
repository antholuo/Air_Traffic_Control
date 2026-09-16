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
    let rotation_dps_default = 2.0;
    let mut auto_rotate = true;

    let mut camera = Camera::new(88.0, 35.0, 0.0, vec2(0.0, 0.0));

    loop {
        clear_background(LIGHTGRAY);

        // Mouse interaction
        let wheel = mouse_wheel();
        if wheel.1 != 0.0 {
            auto_rotate = false;
            camera.radius = (camera.radius - wheel.1 * 5.0).clamp(20.0, 300.0); // set min/max distance
            // with clamp
        }
        if is_mouse_button_down(MouseButton::Left) {
            let delta = mouse_delta_position();
            if delta.length_squared() > 0.0 {
                auto_rotate = false;
                let ctrl_pressed =
                    is_key_down(KeyCode::LeftControl) || is_key_down(KeyCode::RightControl);
                if ctrl_pressed {
                    camera.rotation_degrees -= delta.x * 100.0;
                    camera.elevation_degrees =
                        (camera.elevation_degrees + delta.y * 100.0).clamp(5.0, 85.0);
                } else {
                    let rad = camera.rotation_degrees.to_radians();
                    let right = vec2(-rad.sin(), rad.cos());
                    let forward = vec2(-rad.cos(), -rad.sin());
                    let pan_speed = 0.25;
                    camera.target_xy -= (right * delta.x + forward * delta.y) * pan_speed;
                }
            }
        }

        // auto rotation
        if auto_rotate {
            camera.rotation_degrees += rotation_dps_default * get_frame_time();
        }

        // slices (number of lines)
        // spacing (how far apart)
        draw_grid(100, 1.0, BLACK, GRAY);

        // --- 2D UI OVERLAY PASS ---
        set_default_camera();
        draw_centered_text(
            &format!(
                "Radius: {:.1} | Elevation: {:.1} | Rotation: {:.1}",
                camera.radius, camera.elevation_degrees, camera.rotation_degrees
            ),
            screen_width() / 2.0,
            30.0,
            20.0,
            BLACK,
        );

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
