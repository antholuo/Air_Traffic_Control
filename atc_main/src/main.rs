use macroquad::prelude::*;

fn draw_centered_text(text: &str, center_x: f32, center_y: f32, font_size: f32, color: Color) {
    let text_dims = measure_text(text, None, font_size as u16, 1.0);

    // minus half-width for horizontal center
    let x = center_x - text_dims.width / 2.0;
    let y = center_y + text_dims.height / 2.0;

    // draw_text (text, x, y, font_size, colour)
    // where x, y is bottom-left baseline anchor
    draw_text(text, x, y, font_size, color);
}

#[macroquad::main("AtcMain")]
async fn main() {
    let mut mousepos: (f32, f32) = (0.0, 0.0);
    let mut mouseclick: bool = false;
    loop {
        // runs everytime to clear the background
        clear_background(GRAY);

        // runs everytime in case the screen has been resized
        // screen (0,0) is the top left corner
        let reference_center_x = screen_width() / 2.0; // +x is to the right
        let reference_center_y = screen_height() / 2.0; // +y is down

        let greeting = "Goofy Goomba";
        let font_size = 32.0;
        draw_centered_text(
            greeting,
            reference_center_x,
            reference_center_y,
            font_size,
            WHITE,
        );
        // draw_line(x1, y1, x1, y2, thickness, colour);
        draw_line(0.0, 0.0, 100.0, 100.0, 10.0, BLUE);
        draw_rectangle(screen_width() / 2.0 - 60.0, 100.0, 12.0, 60.0, GREEN);

        if is_mouse_button_pressed(MouseButton::Left) {
            mouseclick = true;

            // TODO: determine how to map screen position to "reference" position
            mousepos = mouse_position();

            // TODO: spawn plane
        }
        if (mouseclick) {
            draw_circle(mousepos.0, mousepos.1, 25.0, RED);
        }

        next_frame().await
    }
}
