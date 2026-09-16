use macroquad::prelude;

pub struct Camera {
    pub radius: f32,
    pub elevation_degrees: f32,
    pub rotation_degrees: f32,
    pub target_xy: prelude::Vec2,
}

impl Camera {
    pub fn new(
        radius: f32,
        elevation_degrees: f32,
        rotation_degrees: f32,
        target_xy: prelude::Vec2,
    ) -> Self {
        Self {
            radius,
            elevation_degrees,
            rotation_degrees,
            target_xy,
        }
    }

    pub fn to_macroquad_camera_3d(&self) -> prelude::Camera3D {
        let elevation_radians = self.elevation_degrees.to_radians();
        let rotation_radians = self.rotation_degrees.to_radians();

        let x = self.target_xy.x + self.radius * elevation_radians.cos() * rotation_radians.sin();
        let y = self.radius * elevation_radians.sin();
        let z = self.target_xy.y + self.radius * elevation_radians.cos() * rotation_radians.cos();

        prelude::Camera3D {
            position: prelude::vec3(x, y, z),
            target: prelude::vec3(self.target_xy.x, 0.0, self.target_xy.y),
            up: prelude::vec3(0.0, 1.0, 0.0),
            ..Default::default()
        }
    }
}
