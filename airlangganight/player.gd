extends CharacterBody3D

const SPEED_WALK = 3.0
const SPEED_CROUCH = 1.5
const SPRINT_MULTIPLIER = 1.6
const MOUSE_SENSITIVITY = 0.003
const GRAVITY = 9.8

@onready var head = $Head
@onready var camera = $Head/Camera3D
@onready var flashlight = $Head/Flashlight

func _ready():
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	flashlight.visible = false

func _unhandled_input(event):
	if event is InputEventMouseMotion:
		head.rotate_y(-event.relative.x * MOUSE_SENSITIVITY)
		camera.rotate_x(-event.relative.y * MOUSE_SENSITIVITY)
		camera.rotation.x = clamp(camera.rotation.x, deg_to_rad(-80), deg_to_rad(80))
	
	if event.is_action_pressed("flashlight"):
		flashlight.visible = !flashlight.visible

func _physics_process(delta):
	if not is_on_floor():
		velocity.y -= GRAVITY * delta

	var current_speed = SPEED_WALK
	if Input.is_action_pressed("crouch"):
		current_speed = SPEED_CROUCH
		head.position.y = 0.8
	else:
		head.position.y = 1.5
		if Input.is_action_pressed("sprint"):
			current_speed *= SPRINT_MULTIPLIER

	var input_dir = Input.get_vector("move_left", "move_right", "move_forward", "move_back")
	var direction = (head.transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()
	
	if direction:
		velocity.x = direction.x * current_speed
		velocity.z = direction.z * current_speed
	else:
		velocity.x = move_toward(velocity.x, 0, current_speed)
		velocity.z = move_toward(velocity.z, 0, current_speed)

	move_and_slide()
