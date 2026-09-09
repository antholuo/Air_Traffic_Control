use macroquad::prelude::*;
use trig::Trig;

fn draw_centered_text(text: &str, center_x: f32, center_y: f32, font_size: f32, color: Color) {
    let text_dims = measure_text(text, None, font_size as u16, 1.0);

    // minus half-width for horizontal center
    let x = center_x - text_dims.width / 2.0;
    let y = center_y + text_dims.height / 2.0;

    // draw_text (text, x, y, font_size, colour)
    // where x, y is bottom-left baseline anchor
    draw_text(text, x, y, font_size, color);
}

fn deg_to_coord(radius: f32, degrees: f32) -> (f32, f32) {
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
    let cam_radius: f32 = 80.0;
    let cam_y: f32 = 50.0;
    let cam_rotation_dps: f32 = 2.0;
    let mut cam_rotation_angle: f32 = 0.0;
    loop {
        clear_background(LIGHTGRAY);

        // calculate camera rotation
        cam_rotation_angle += cam_rotation_dps * get_frame_time(); // Rotate N degrees per second
        //

        let (cam_x, cam_z) = deg_to_coord(cam_radius, cam_rotation_angle);

        // Set the camera
        // Note: I think position is x/y/z?
        set_camera(&Camera3D {
            position: vec3(cam_x, cam_y, cam_z),
            target: vec3(0.0, 0.0, 0.0),
            up: vec3(0.0, 1.0, 0.0),
            ..Default::default() // rest of the fields that I'm not gonna bother with for now
        });

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
