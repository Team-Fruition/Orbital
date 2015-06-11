import cx_Freeze;

executables = [cx_Freeze.Executable("main.py")];

packages = ["pygame"];
includefiles = ["Art_Assets/",
                "BulletObjects.py",
                "DisplacementController.py",
                "Object.py",
                "ObjectStorage.py",
                "Scene.py",
                "SceneManager.py",
                "ShipObjects.py",
                "SpeedController.py",
                "supplementary.py",
                "UIObjects.py",
                "WeaponObjects.py"];

cx_Freeze.setup(
    name = "Space Arena",
    version = "0.1",
    options = {"build_exe":{"packages":packages,
                            "include_files":includefiles}},
    description = "Space Arena",
    executables = executables
    )
