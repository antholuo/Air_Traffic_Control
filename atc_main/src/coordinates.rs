use macroquad::prelude::*;

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct AirspaceCoords(pub Vec3); // 3d coordinates we reference inside of our world

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct ScreenCoords(pub Vec3); // 3d coordinates on the screen

impl AirspaceCoords {
    pub fn visualize_on_screen(&self) -> Vec3 {
        // TODO: implement a set of scaling so that things make sense on screen
        let scale: f32 = 0.1;
        vec3(self.0.x, self.0.y * alt_scale, self.0.z) // bc only one field in airspace coords!
        // (Maybe we put scaling in there? dunno)
    }
}

