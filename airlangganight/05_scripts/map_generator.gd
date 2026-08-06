@tool
extends Node3D

@export var build_map_now: bool = false:
	set(val):
		if val:
			generate_school_map()
			build_map_now = false

func generate_school_map():
	# Hapus map lama jika ada
	var old_map = get_node_or_null("GeneratedMap")
	if old_map:
		old_map.free()
		
	var map_node = Node3D.new()
	map_node.name = "GeneratedMap"
	add_child(map_node)
	
	# Ambil root scene dengan aman
	var root_node = Engine.get_main_loop().get_edited_scene_root()
	if root_node:
		map_node.owner = root_node
	
	# 1. LANTAI UTAMA (30x40m)
	create_box(map_node, "Lantai_Utama", Vector3(30, 0.2, 40), Vector3(0, -0.1, 0), root_node)
	
	# 2. DINDING LUAR / PAGAR
	create_box(map_node, "Dinding_Kiri", Vector3(0.5, 4, 40), Vector3(-15, 2, 0), root_node)
	create_box(map_node, "Dinding_Kanan", Vector3(0.5, 4, 40), Vector3(15, 2, 0), root_node)
	create_box(map_node, "Dinding_Belakang", Vector3(30, 4, 0.5), Vector3(0, 2, -20), root_node)
	
	# 3. LAB PPLG (Lantai 1 / Depan)
	create_box(map_node, "Dinding_Lab_1", Vector3(12, 4, 0.5), Vector3(-8, 2, -5), root_node)
	create_box(map_node, "Dinding_Lab_Sekat", Vector3(0.5, 4, 12), Vector3(-2, 2, -11), root_node)
	
	# 4. RUANG ELEKTRIKAL (Belakang)
	create_box(map_node, "Dinding_Elektrikal", Vector3(10, 4, 0.5), Vector3(9, 2, -8), root_node)
	
	# 5. GERBANG UTAMA (Pintu Keluar)
	create_box(map_node, "Gerbang_Kiri", Vector3(10, 4, 0.5), Vector3(-10, 2, 20), root_node)
	create_box(map_node, "Gerbang_Kanan", Vector3(10, 4, 0.5), Vector3(10, 2, 20), root_node)

func create_box(parent: Node, box_name: String, size: Vector3, pos: Vector3, root_node: Node):
	var csg = CSGBox3D.new()
	csg.name = box_name
	csg.size = size
	csg.position = pos
	csg.use_collision = true
	parent.add_child(csg)
	if root_node:
		csg.owner = root_node
