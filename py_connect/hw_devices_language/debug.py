from os.path import join, dirname
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export


def main(debug=False):

    this_folder = dirname(__file__)

    hw_mm = metamodel_from_file(join(this_folder, 'hw_devices.tx'), debug=False)
    #metamodel_export(hw_mm, join(this_folder, 'robot_meta.dot'))

    # Register object processor for MoveCommand
    #hw_mm.register_obj_processors({'MoveCommand': move_command_processor})

    robot_model = hw_mm.model_from_file(join(this_folder, 'debug.hwd'))
    #model_export(robot_model, join(this_folder, 'program.dot'))

    print((robot_model))
    print(dir(robot_model))
    print(robot_model.attrs)
    print(robot_model.attrs[0].name)
    print(robot_model.attrs[3].val.rom.unit)
    print(robot_model.attrs[4].val)
    print(robot_model.attrs[4].val[0].freq)
    print(robot_model.attrs[5].version)
    print(robot_model.attrs[11].val.fpu)
    #robot = Robot()
    #robot.interpret(robot_model)


if __name__ == "__main__":
    main()
