from pathlib import Path

from universe_sim import Player, UniverseSim, Vehicle
from universe_sim.admin.builder import AdminBackendPanel, BuilderMenu
from universe_sim.apps.vos import VOSShell
from universe_sim.models import AuditLogEntry


def build_sim() -> UniverseSim:
    return UniverseSim(Path.cwd())


def test_interaction_loop_pickup_open_vehicle_retrieve():
    sim = build_sim()
    player = Player(player_id="p1")
    vehicle = Vehicle(vehicle_id="v1")
    sim.add_vehicle(vehicle)

    device = sim.spawn_device("laptop")
    sim.pickup(player, device.device_id)
    sim.open_device(device.device_id)
    sim.place_on_surface(player, device.device_id, "table")
    sim.pickup(player, device.device_id)
    sim.store_in_vehicle(player, device.device_id, vehicle)
    sim.retrieve_from_vehicle(player, device.device_id, vehicle)

    assert player.carry_slot == device.device_id


def test_persistence_open_edit_close_move_reopen(tmp_path: Path):
    sim = build_sim()
    player = Player(player_id="p1")
    vehicle = Vehicle(vehicle_id="v1")
    sim.add_vehicle(vehicle)

    device = sim.spawn_device("laptop")
    sim.pickup(player, device.device_id)
    sim.open_device(device.device_id)
    sim.write_file(device.device_id, "/home/note1.txt", "notes", "Persistent note")
    sim.close_device(device.device_id)
    sim.store_in_vehicle(player, device.device_id, vehicle)

    save = tmp_path / "world.json"
    sim.save_world(save)

    sim2 = build_sim()
    sim2.load_world(save)
    sim2.open_device(device.device_id)
    assert sim2.devices[device.device_id].files["/home/note1.txt"].content == "Persistent note"


def test_admin_permissions_and_audit():
    sim = build_sim()
    non_admin = Player(player_id="u1", is_admin=False)
    admin = Player(player_id="a1", is_admin=True)
    builder = BuilderMenu(sim)

    try:
        builder.create_app_template(non_admin, {"name": "Nope", "permissions": []})
        raised = False
    except PermissionError:
        raised = True

    assert raised

    builder.create_app_template(admin, {"name": "Field Ops", "permissions": ["files"], "layout": "panel"})
    assert any(e.action == "create_app_template" for e in sim.audit_log)


def test_storage_quota_enforced():
    sim = build_sim()
    device = sim.spawn_device("tablet")
    sim.write_file(device.device_id, "/home/a.txt", "notes", "a" * 200)

    try:
        sim.write_file(device.device_id, "/home/b.txt", "notes", "b" * 200)
        sim.write_file(device.device_id, "/home/c.txt", "notes", "c" * 200)
        raised = False
    except ValueError:
        raised = True

    assert raised


def test_backend_device_blueprint_and_spawn():
    sim = build_sim()
    admin = Player(player_id="a1", is_admin=True)
    backend = AdminBackendPanel(sim)
    backend.create_device_blueprint(
        admin,
        {
            "type_id": "server_case",
            "name": "Server Case",
            "weight": 8.1,
            "size": 5,
            "durability": 90,
            "battery_capacity": 50,
            "storage_capacity": 2048,
            "supports_hinge": False,
            "mount_compatible": True,
        },
    )
    device = sim.spawn_device("server_case")
    assert device.definition.name == "Server Case"


def test_audit_10_actions():
    sim = build_sim()
    for i in range(10):
        sim.log_admin_action(
            AuditLogEntry(actor_id="admin", action=f"action_{i}", target="t", location="/admin", metadata={"i": i})
        )
    assert len(sim.audit_log) == 10


def test_stress_20_devices_5_vehicles_vos_running():
    sim = build_sim()
    shell = VOSShell(sim)
    devices = [sim.spawn_device("laptop") for _ in range(20)]
    vehicles = [Vehicle(vehicle_id=f"v{i}") for i in range(5)]
    for v in vehicles:
        sim.add_vehicle(v)

    for i, device in enumerate(devices):
        shell.boot(device.device_id)
        sim.launch_app(device.device_id, "Settings")
        if i < 5:
            p = Player(player_id=f"p{i}")
            sim.pickup(p, device.device_id)
            sim.store_in_vehicle(p, device.device_id, vehicles[i])
            sim.charge_from_vehicle(device.device_id, has_adapter=True)

    assert all(d.state.power_on for d in devices)
    assert sum(len(v.cargo_inventory.items) for v in vehicles) == 5


def test_vos_desktop_metadata_exists():
    sim = build_sim()
    shell = VOSShell(sim)
    device = sim.spawn_device("rugged_laptop")
    screen = shell.boot(device.device_id, login_required=False)
    desktop = shell.desktop(device.device_id)

    assert screen == "desktop"
    assert "/home" in desktop["directories"]
    assert "Builder Console" in desktop["dock"]
