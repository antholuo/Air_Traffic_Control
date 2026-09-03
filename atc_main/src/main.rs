use macroquad::prelude::*;

fn draw_centered_text(text: &str, center_x: f32, center_y: f32, font_size: f32, color: Color) {
    let text_dims = measure_text(text, None, font_size as u16, 1.0);

    // minus half-width for horizontal center
    let x = center_x - text_dims.width / 2.0;
    let y = center_y + text_dims.height / 2.0;

    draw_text(text, x, y, font_size, color);
}

#[macroquad::main("AtcMain")]
async fn main() {
    let mut mouseclick: bool = false;
    loop {
        clear_background(GRAY);
        let screen_center_x = screen_width() / 2.0;
        let screen_center_y = screen_height() / 2.0;

        let greeting = "Goofy Goomba";
        let font_size = 32.0;

        draw_centered_text(greeting, screen_center_x, screen_center_y, font_size, WHITE);

        // draw_line(x1, y1, x1, y2, thickness, colour);
        draw_line(0.0, 0.0, 100.0, 100.0, 10.0, BLUE);
        draw_rectangle(screen_width() / 2.0 - 60.0, 100.0, 12.0, 60.0, GREEN);

        if is_mouse_button_pressed(MouseButton::Left) {
            mouseclick = true;
        }
        if (mouseclick) {
            // draw_text (text, x, y, font_size, colour)
            // where x, y is bottom-left baseline anchor
            draw_text("Hello, Macrquad!", 20.0, 20.0, 30.0, RED);
        }

        next_frame().await
    }
}
