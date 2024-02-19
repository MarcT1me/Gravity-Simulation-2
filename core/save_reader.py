import PhEngineV2

from core.planet import Planet, Satellite


def get_tuple(string, intype) -> tuple:
    return tuple(map(intype, string.replace('(', '').replace(')', '').split(', ')))


def read_save(save_name, *, save_path=PhEngineV2.config.SAVES_path) -> str:
    """ reading a text save """
    with open(rf'{PhEngineV2.config.APPLICATION_PATH}/{save_path}/{save_name}.syssav', mode='r') as save_file:
        lines = save_file.readlines()
        
        version = lines[0]
        for line in lines[1::]:
            if line[0] == '#':
                continue
            line_commands = line.split('|')
            print(f'Sav - line: {line_commands[0]};   opt: {line_commands[1::]}')
            
            if line_commands[0] == 'Planet':
                PhEngineV2.scene.add(
                    Planet(
                        body_id=line_commands[1],
                        pos=get_tuple(line_commands[2], float),
                        velocity=get_tuple(line_commands[3], float),
                        mass=float(line_commands[4]),
                        size=get_tuple(line_commands[5], float),
                        color=get_tuple(line_commands[6], int)
                    )
                )
            elif line_commands[0] == 'Satellite':
                PhEngineV2.scene.add(
                    Satellite(
                        body_id=line_commands[1],
                        pos=get_tuple(line_commands[2], float),
                        velocity=get_tuple(line_commands[3], float),
                        mass=float(line_commands[4]),
                        size=get_tuple(line_commands[5], float),
                        color=get_tuple(line_commands[6], int),
                        offset=get_tuple(line_commands[7], int)
                    )
                )
    
    print('\nSav - read\n\n')
    return version


def write_sav(save_name, *, save_path=PhEngineV2.config.SAVES_path) -> str:
    """ writing a text save """
    with open(rf'{PhEngineV2.config.APPLICATION_PATH}/{save_path}/{save_name}.syssav', mode='w') as file:
        file.write(PhEngineV2.config.APPLICATION_VERSION)
        
        for body in PhEngineV2.scene.entities.values():
            s = '\n'
            
            # type
            if isinstance(body, Planet):
                s += 'Planet' + '|'
                s += body.id + '|'
                s += str(body.pos) + '|'
                s += str(body.speed) + '|'
                s += str(body.mass) + '|'
                s += str(body.size) + '|'
                s += str(body.albedo)
            elif isinstance(body, Satellite):
                s += 'Satellite' + '|'
                s += body.id + '|'
                s += str(body.pos) + '|'
                s += str(body.speed) + '|'
                s += str(body.mass) + '|'
                s += str(body.size) + '|'
                s += str(body.albedo) + '|'
                s += str(tuple(body.offset))
            
            file.write(s)
