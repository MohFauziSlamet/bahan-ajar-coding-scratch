const fs = require('fs');
const path = require('path');
const { renderBlockToFiles } = require('./renderer.js');

const outDir = path.join(__dirname, '../junkins-lomba-coding-scatch/images/modul02');
fs.mkdirSync(outDir, { recursive: true });

const blocks = [
    // BABAK 1 - Player
    {
        name: 'b1_player_init',
        code: `when flag clicked
hide`
    },
    {
        name: 'b1_player_movement',
        code: `when I receive [Start_Babak1 v]
show
set rotation style [left-right v]
go to x: (-160) y: (-80)
switch costume to [pejuang_idle v]
set [is_attacking v] to [false]
forever
  if <(GameState) = [Babak1]> then
    if <<key [right arrow v] pressed?> or <key [d v] pressed?>> then
      point in direction (90)
      change x by (6)
      next costume
    end
    if <<key [left arrow v] pressed?> or <key [a v] pressed?>> then
      point in direction (-90)
      change x by (-6)
      next costume
    end
    if <(x position) < (-210)> then
      set x to (-210)
    end
    if <(x position) > (180)> then
      set x to (180)
    end
    if <<key [space v] pressed?> and <(is_attacking) = [false]>> then
      set [is_attacking v] to [true]
      start sound [sfx_swing v]
      switch costume to [pejuang_tusuk v]
      wait (0.2) seconds
      switch costume to [pejuang_idle v]
      wait (0.1) seconds
      set [is_attacking v] to [false]
    end
  else
    hide
    stop [this script v]
  end
end`
    },
    {
        name: 'b1_player_hurt',
        code: `when I receive [Player_Hurt_Babak1 v]
repeat (2)
  set [ghost v] effect to (60)
  wait (0.08) seconds
  set [ghost v] effect to (0)
  wait (0.08) seconds
end`
    },

    // BABAK 1 - Enemy
    {
        name: 'b1_enemy_init',
        code: `when flag clicked
hide`
    },
    {
        name: 'b1_enemy_spawner',
        code: `when I receive [Start_Babak1 v]
hide
forever
  if <(GameState) = [Babak1]> then
    wait (pick random (1.8) to (3.2)) seconds
    create clone of [myself v]
  else
    stop [this script v]
  end
end`
    },
    {
        name: 'b1_enemy_clone_logic',
        code: `when I start as a clone
show
set rotation style [left-right v]
point in direction (-90)
go to x: (240) y: (-80)
set [enemy_speed v] to (pick random (3) to (5))
forever
  if <(GameState) = [Babak1]> then
    change x by (0 - (enemy_speed))
    if <touching [Player_Babak1 v]?> then
      if <([is_attacking v] of [Player_Babak1]) = [true]> then
        start sound [sfx_hit_enemy v]
        change [Score v] by (10)
        if <(Score) > (99)> then
          broadcast [Level_Clear v]
        end
        repeat (4)
          change [ghost v] effect by (25)
          change y by (4)
          wait (0.04) seconds
        end
        delete this clone
      else
        change [Lives v] by (-1)
        start sound [sfx_player_hurt v]
        broadcast [Player_Hurt_Babak1 v]
        delete this clone
      end
    end
    if <(x position) < (-235)> then
      delete this clone
    end
  else
    delete this clone
  end
end`
    },

    // BABAK 2 - Player
    {
        name: 'b2_player_init',
        code: `when flag clicked
hide`
    },
    {
        name: 'b2_player_aim_shoot',
        code: `when I receive [Start_Babak2 v]
show
go to x: (-150) y: (-60)
set [can_shoot v] to [true]
forever
  if <(GameState) = [Babak2]> then
    point towards [mouse-pointer v]
    if <(direction) < (0)> then
      point in direction (0)
    end
    if <(direction) > (180)> then
      point in direction (180)
    end
    if <<key [up arrow v] pressed?> or <key [w v] pressed?>> then
      change y by (4)
    end
    if <<key [down arrow v] pressed?> or <key [s v] pressed?>> then
      change y by (-4)
    end
    if <(y position) < (-120)> then
      set y to (-120)
    end
    if <(y position) > (20)> then
      set y to (20)
    end
    if <<mouse down?> and <(can_shoot) = [true]>> then
      set [can_shoot v] to [false]
      start sound [sfx_gunfire v]
      broadcast [Spawn_Bullet v]
      change x by (-5)
      wait (0.05) seconds
      change x by (5)
      wait (0.25) seconds
      set [can_shoot v] to [true]
    end
  else
    hide
    stop [this script v]
  end
end`
    },

    // BABAK 2 - Bullet
    {
        name: 'b2_bullet_init',
        code: `when flag clicked
hide`
    },
    {
        name: 'b2_bullet_receiver',
        code: `when I receive [Spawn_Bullet v]
if <(GameState) = [Babak2]> then
  create clone of [myself v]
end`
    },
    {
        name: 'b2_bullet_clone_logic',
        code: `when I start as a clone
show
go to [Player_Babak2 v]
point in direction ([direction v] of [Player_Babak2])
move (25) steps
repeat until <<touching [edge v]?> or <touching [Enemy_Surabaya v]?>>
  move (16) steps
end
if <touching [Enemy_Surabaya v]?> then
  start sound [sfx_impact v]
  delete this clone
end
if <touching [edge v]?> then
  delete this clone
end`
    },

    // BABAK 2 - Enemy
    {
        name: 'b2_enemy_init',
        code: `when flag clicked
hide`
    },
    {
        name: 'b2_enemy_spawner',
        code: `when I receive [Start_Babak2 v]
hide
forever
  if <(GameState) = [Babak2]> then
    wait (pick random (1.5) to (2.8)) seconds
    create clone of [myself v]
  else
    stop [this script v]
  end
end`
    },
    {
        name: 'b2_enemy_clone_logic',
        code: `when I start as a clone
show
go to x: (240) y: (pick random (-100) to (10))
set [enemy_health v] to (2)
forever
  if <(GameState) = [Babak2]> then
    change x by (-2.5)
    if <touching [Bullet_Player v]?> then
      change [enemy_health v] by (-1)
      set [brightness v] effect to (50)
      wait (0.05) seconds
      set [brightness v] effect to (0)
      if <(enemy_health) < (1)> then
        change [Score v] by (20)
        start sound [sfx_enemy_down v]
        if <(Score) > (249)> then
          broadcast [Level_Clear v]
        end
        delete this clone
      end
    end
    if <(x position) < (-220)> then
      change [Lives v] by (-1)
      start sound [sfx_alarm v]
      delete this clone
    end
  else
    delete this clone
  end
end`
    }
];

async function generateAll() {
    console.log('Generating', blocks.length, 'Scratch puzzle blocks for Modul 02...');
    for (const b of blocks) {
        await renderBlockToFiles(b.code, b.name, outDir);
    }
    console.log('All Modul 02 blocks successfully generated in:', outDir);
}

generateAll();
