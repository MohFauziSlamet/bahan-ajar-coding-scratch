const fs = require('fs');
const path = require('path');
const { renderBlockToFiles } = require('./renderer.js');

const outDir = path.join(__dirname, '../junkins-lomba-coding-scatch/images/modul03');
fs.mkdirSync(outDir, { recursive: true });

const blocks = [
    // BABAK 3: Player Plane
    {
        name: 'b3_player_init',
        code: `when flag clicked
hide`
    },
    {
        name: 'b3_player_movement',
        code: `when I receive [Start_Babak3 v]
show
go to x: (-160) y: (0)
set rotation style [don't rotate v]
forever
  if <(GameState) = [Babak3]> then
    if <<key [up arrow v] pressed?> or <key [w v] pressed?>> then
      change y by (6)
    end
    if <<key [down arrow v] pressed?> or <key [s v] pressed?>> then
      change y by (-6)
    end
    if <<key [right arrow v] pressed?> or <key [d v] pressed?>> then
      change x by (6)
    end
    if <<key [left arrow v] pressed?> or <key [a v] pressed?>> then
      change x by (-6)
    end
    if <(y position) > (150)> then
      set y to (150)
    end
    if <(y position) < (-150)> then
      set y to (-150)
    end
    if <(x position) < (-210)> then
      set x to (-210)
    end
    if <(x position) > (180)> then
      set x to (180)
    end
    if <key [space v] pressed?> then
      start sound [sfx_plane_shoot v]
      broadcast [Spawn_Air_Bullet v]
      wait (0.2) seconds
    end
  else
    hide
    stop [this script v]
  end
end`
    },
    {
        name: 'b3_player_hurt',
        code: `when I receive [Player_Hurt_Babak3 v]
repeat (3)
  set [ghost v] effect to (60)
  wait (0.06) seconds
  set [ghost v] effect to (0)
  wait (0.06) seconds
end`
    },

    // BABAK 3: Air Bullet
    {
        name: 'b3_bullet_init',
        code: `when flag clicked
hide`
    },
    {
        name: 'b3_bullet_receiver',
        code: `when I receive [Spawn_Air_Bullet v]
if <(GameState) = [Babak3]> then
  create clone of [myself v]
end`
    },
    {
        name: 'b3_bullet_clone_logic',
        code: `when I start as a clone
show
go to [Player_Plane_Babak3 v]
point in direction (90)
change x by (20)
repeat until <<touching [edge v]?> or <touching [Enemy_Plane v]?>>
  change x by (18)
end
if <touching [Enemy_Plane v]?> then
  start sound [sfx_impact v]
  delete this clone
end
if <touching [edge v]?> then
  delete this clone
end`
    },

    // BABAK 3: Enemy Plane
    {
        name: 'b3_enemy_init',
        code: `when flag clicked
hide`
    },
    {
        name: 'b3_enemy_spawner',
        code: `when I receive [Start_Babak3 v]
hide
forever
  if <(GameState) = [Babak3]> then
    wait (pick random (1.5) to (2.8)) seconds
    create clone of [myself v]
  else
    stop [this script v]
  end
end`
    },
    {
        name: 'b3_enemy_clone_logic',
        code: `when I start as a clone
show
go to x: (240) y: (pick random (-120) to (120))
set [enemy_speed v] to (pick random (4) to (7))
forever
  if <(GameState) = [Babak3]> then
    change x by (0 - (enemy_speed))
    change y by ((sin of ((x position) * (3))) * (4))
    if <touching [Bullet_Air v]?> then
      start sound [sfx_explosion v]
      change [Score v] by (25)
      if <(Score) > (499)> then
        broadcast [Level_Clear v]
      end
      repeat (3)
        change [ghost v] effect by (30)
        wait (0.04) seconds
      end
      delete this clone
    end
    if <touching [Player_Plane_Babak3 v]?> then
      change [Lives v] by (-1)
      start sound [sfx_player_hurt v]
      broadcast [Player_Hurt_Babak3 v]
      delete this clone
    end
    if <(x position) < (-235)> then
      delete this clone
    end
  else
    delete this clone
  end
end`
    },

    // BABAK 3: Cloud Scroller (Parallax)
    {
        name: 'b3_cloud_init',
        code: `when flag clicked
hide`
    },
    {
        name: 'b3_cloud_spawner',
        code: `when I receive [Start_Babak3 v]
hide
forever
  if <(GameState) = [Babak3]> then
    wait (pick random (1.0) to (2.5)) seconds
    create clone of [myself v]
  else
    stop [this script v]
  end
end`
    },
    {
        name: 'b3_cloud_clone_logic',
        code: `when I start as a clone
go to [back v] layer
go to x: (250) y: (pick random (-160) to (160))
set size to (pick random (50) to (120)) %
set [ghost v] effect to (pick random (30) to (60))
show
repeat until <(x position) < (-250)>
  change x by (-5)
end
delete this clone`
    },

    // BABAK 4: Player Space Mecha Jet
    {
        name: 'b4_player_init',
        code: `when flag clicked
hide`
    },
    {
        name: 'b4_player_controls',
        code: `when I receive [Start_Babak4 v]
show
go to x: (0) y: (-120)
set rotation style [don't rotate v]
forever
  if <(GameState) = [Babak4]> then
    if <<key [left arrow v] pressed?> or <key [a v] pressed?>> then
      change x by (-7)
    end
    if <<key [right arrow v] pressed?> or <key [d v] pressed?>> then
      change x by (7)
    end
    if <<key [up arrow v] pressed?> or <key [w v] pressed?>> then
      change y by (6)
    end
    if <<key [down arrow v] pressed?> or <key [s v] pressed?>> then
      change y by (-6)
    end
    if <(x position) < (-210)> then
      set x to (-210)
    end
    if <(x position) > (210)> then
      set x to (210)
    end
    if <(y position) < (-150)> then
      set y to (-150)
    end
    if <(y position) > (-30)> then
      set y to (-30)
    end
    if <<mouse down?> or <key [space v] pressed?>> then
      start sound [sfx_laser v]
      broadcast [Spawn_Space_Laser v]
      wait (0.18) seconds
    end
  else
    hide
    stop [this script v]
  end
end`
    },
    {
        name: 'b4_player_hurt',
        code: `when I receive [Player_Hurt_Babak4 v]
repeat (3)
  set [ghost v] effect to (60)
  wait (0.06) seconds
  set [ghost v] effect to (0)
  wait (0.06) seconds
end`
    },

    // BABAK 4: Laser Player
    {
        name: 'b4_laser_init',
        code: `when flag clicked
hide`
    },
    {
        name: 'b4_laser_receiver',
        code: `when I receive [Spawn_Space_Laser v]
if <(GameState) = [Babak4]> then
  create clone of [myself v]
end`
    },
    {
        name: 'b4_laser_clone_logic',
        code: `when I start as a clone
show
go to [Player_Space_Babak4 v]
point in direction (0)
change y by (20)
repeat until <<touching [edge v]?> or <touching [Boss_Antariksa v]?>>
  change y by (20)
end
if <touching [Boss_Antariksa v]?> then
  start sound [sfx_impact v]
  delete this clone
end
if <touching [edge v]?> then
  delete this clone
end`
    },

    // BABAK 4: Boss Antariksa (Final Boss)
    {
        name: 'b4_boss_init',
        code: `when flag clicked
hide`
    },
    {
        name: 'b4_boss_ai_patrol',
        code: `when I receive [Start_Babak4 v]
show
go to x: (0) y: (100)
set [Boss_HP v] to (20)
set [boss_dir v] to (5)
forever
  if <(GameState) = [Babak4]> then
    change x by (boss_dir)
    if <(x position) > (180)> then
      set [boss_dir v] to (-5)
    end
    if <(x position) < (-180)> then
      set [boss_dir v] to (5)
    end
    if <(pick random (1) to (20)) = (1)> then
      broadcast [Boss_Fire_Laser v]
    end
  else
    hide
    stop [this script v]
  end
end`
    },
    {
        name: 'b4_boss_hit_damage',
        code: `when I receive [Start_Babak4 v]
forever
  if <(GameState) = [Babak4]> then
    if <touching [Laser_Player v]?> then
      change [Boss_HP v] by (-1)
      set [brightness v] effect to (60)
      wait (0.05) seconds
      set [brightness v] effect to (0)
      if <(Boss_HP) < (1)> then
        start sound [sfx_big_explosion v]
        change [Score v] by (200)
        repeat (10)
          change [ghost v] effect by (10)
          change size by (5) %
          wait (0.05) seconds
        end
        broadcast [Level_Clear v]
        hide
        stop [this script v]
      end
    end
  else
    stop [this script v]
  end
end`
    },

    // BABAK 4: Boss Laser Enemy
    {
        name: 'b4_boss_laser_init',
        code: `when flag clicked
hide`
    },
    {
        name: 'b4_boss_laser_receiver',
        code: `when I receive [Boss_Fire_Laser v]
if <(GameState) = [Babak4]> then
  create clone of [myself v]
end`
    },
    {
        name: 'b4_boss_laser_clone_logic',
        code: `when I start as a clone
show
go to [Boss_Antariksa v]
point in direction (180)
change y by (-30)
repeat until <<touching [edge v]?> or <touching [Player_Space_Babak4 v]?>>
  change y by (-10)
end
if <touching [Player_Space_Babak4 v]?> then
  change [Lives v] by (-1)
  start sound [sfx_player_hurt v]
  broadcast [Player_Hurt_Babak4 v]
  delete this clone
end
if <touching [edge v]?> then
  delete this clone
end`
    }
];

async function generateAll() {
    console.log('Generating', blocks.length, 'Scratch puzzle blocks for Modul 03...');
    for (const b of blocks) {
        await renderBlockToFiles(b.code, b.name, outDir);
    }
    console.log('All Modul 03 blocks successfully generated in:', outDir);
}

generateAll();
