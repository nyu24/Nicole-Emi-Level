init -5 python:
    def use_backing_card():
        renpy.hide_screen("inventory")
        renpy.jump("sample")
    def use_evidence_bag():
        renpy.hide_screen("inventory")
        renpy.jump("sample")
    def can_magnetic_powder():
        renpy.hide_screen("inventory")
        renpy.jump("canMagneticPowder")
    def use_uv_light():
        renpy.hide_screen("inventory")
        renpy.jump("useUVLight")