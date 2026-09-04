use macroquad::prelude::*;

#[derive(Copy, Clone, Debug)]
pub struct ReferenceCoords(pub Vec2);

#[derive(Copy, Clone, Debug)]
pub struct ScreenCoords(pub Vec2);

// TODO: To/from screen coords once I determine what system for coordinates I'm actually going to
// use
