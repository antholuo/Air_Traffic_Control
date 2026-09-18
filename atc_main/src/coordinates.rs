use macroquad::prelude::*;

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct NauticalMiles(pub f32);

impl NauticalMiles {
    pub const TO_FEET: f32 = 6076.12;

    pub fn to_feet(self) -> Feet {
        NauticalMiles(self.0 * Self::TO_NM)
    }
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Feet(pub f32);

impl Feet {
    pub const TO_NM: f32 = 1.0 / 6076.12;

    pub fn to_nm(self) -> NauticalMiles {
        Feet(self.0 * Self::TO_NM)
    }
}

/// Airspace Vecs are represented using true units
/// Note that x/z are ground plane location
/// and Y is vertical height
/// at some point we might also need to make some sort of conversion for global gps position but
/// meh we'll do it later
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct AirspaceCoords {
    pub x: NauticalMiles,
    pub y: Feet,
    pub z: NauticalMiles,
}

impl AirspaceCoords {
    pub fn new(x_nm: f32, y_ft: f32, z_nm: f32) -> Self {
        Self {
            x: NauticalMiles(x_nm),
            y: Feet(y_ft),
            z: NauticalMiles(z_nm),
        }
    }

    pub fn to_macroquad_vec3(&self, nm_scale: f32, alt_scale: f32) -> Vec3 {
        vec3(
            self.x.0 * nm_scale,
            self.y.0 * alt_scale,
            self.z.0 * nm_scale,
        )
    }
}

/// world coordinates
/// We apply some amount of altitude scaling to make everything look reasonable
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct ScreenCoords(pub Vec3);
