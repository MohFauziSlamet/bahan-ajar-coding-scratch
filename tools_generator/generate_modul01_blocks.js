const fs = require('fs');
const path = require('path');
const { renderBlockToFiles } = require('./renderer.js');

const outDir = path.join(__dirname, '../junkins-lomba-coding-scatch/images/modul01');
fs.mkdirSync(outDir, { recursive: true });

const blocks = [
    {
        name: 'stage_stack1',
        code: `when flag clicked
set [GameState v] to [Menu]
set [Score v] to (0)
set [Lives v] to (3)
set [CurrentLevel v] to (1)
switch backdrop to [bg_menu v]
stop all sounds
start sound [bgm_patriotik v]
broadcast [Show_Menu v]`
    },
    {
        name: 'stage_stack2',
        code: `when I receive [Start_New_Game v]
set [Score v] to (0)
set [Lives v] to (3)
set [CurrentLevel v] to (1)
broadcast [Tampilkan_Cerita_1 v] and wait
set [GameState v] to [Babak1]
switch backdrop to [bg_babak1 v]
broadcast [Start_Babak1 v]`
    },
    {
        name: 'stage_stack3',
        code: `when I receive [Level_Clear v]
if <(CurrentLevel) = (1)> then
  set [CurrentLevel v] to (2)
  broadcast [Tampilkan_Cerita_2 v] and wait
  set [GameState v] to [Babak2]
  switch backdrop to [bg_babak2 v]
  broadcast [Start_Babak2 v]
else
  if <(CurrentLevel) = (2)> then
    set [CurrentLevel v] to (3)
    broadcast [Tampilkan_Cerita_3 v] and wait
    set [GameState v] to [Babak3]
    switch backdrop to [bg_babak3 v]
    broadcast [Start_Babak3 v]
  else
    if <(CurrentLevel) = (3)> then
      set [CurrentLevel v] to (4)
      broadcast [Tampilkan_Cerita_4 v] and wait
      set [GameState v] to [Babak4]
      switch backdrop to [bg_babak4 v]
      broadcast [Start_Babak4 v]
    else
      if <(CurrentLevel) = (4)> then
        set [GameState v] to [Victory]
        switch backdrop to [bg_victory v]
        stop all sounds
        start sound [sfx_victory v]
        broadcast [Show_Victory_Screen v]
      end
    end
  end
end`
    },
    {
        name: 'stage_stack4',
        code: `when I receive [Trigger_Game_Over v]
if <not <(GameState) = [GameOver]>> then
  set [GameState v] to [GameOver]
  switch backdrop to [bg_gameover v]
  stop all sounds
  start sound [sfx_gameover v]
  broadcast [Show_Game_Over_Screen v]
end`
    },
    {
        name: 'btn_play_stack1',
        code: `when flag clicked
hide`
    },
    {
        name: 'btn_play_stack2',
        code: `when I receive [Show_Menu v]
go to [front v] layer
go to x: (0) y: (-40)
set size to (100) %
show`
    },
    {
        name: 'btn_play_stack3',
        code: `when this sprite clicked
if <(GameState) = [Menu]> then
  start sound [sfx_click v]
  hide
  broadcast [Start_New_Game v]
end`
    },
    {
        name: 'btn_play_stack4',
        code: `when I receive [Trigger_Game_Over v]
hide

when I receive [Show_Victory_Screen v]
hide`
    },
    {
        name: 'dialog_stack1',
        code: `when flag clicked
hide`
    },
    {
        name: 'dialog_stack2',
        code: `when I receive [Tampilkan_Cerita_1 v]
go to [front v] layer
go to x: (0) y: (-120)
show
say [Tahun 1945: Penjajah datang kembali. Berbekal bambu runcing dan tekad baja, para pejuang bangkit! (Tekan SPASI / Klik)]
wait (0.5) seconds
wait until <<key [space v] pressed?> or <mouse down?>>
start sound [sfx_click v]
say []
hide`
    },
    {
        name: 'dialog_stack3',
        code: `when I receive [Tampilkan_Cerita_2 v]
go to [front v] layer
go to x: (0) y: (-120)
show
say [10 November 1945: Arek-arek Suroboyo dan TNI bersatu di Jembatan Merah. Pertahankan kedaulatan! (Tekan SPASI / Klik)]
wait (0.5) seconds
wait until <<key [space v] pressed?> or <mouse down?>>
start sound [sfx_click v]
say []
hide`
    },
    {
        name: 'dialog_stack4',
        code: `when I receive [Tampilkan_Cerita_3 v]
go to [front v] layer
go to x: (0) y: (-120)
show
say [Kedaulatan Dirgantara: Rajawali TNI AU mengudara menjaga langit Nusantara! (Tekan SPASI / Klik)]
wait (0.5) seconds
wait until <<key [space v] pressed?> or <mouse down?>>
start sound [sfx_click v]
say []
hide`
    },
    {
        name: 'dialog_stack5',
        code: `when I receive [Tampilkan_Cerita_4 v]
go to [front v] layer
go to x: (0) y: (-120)
show
say [Masa Depan: Sains & teknologi antariksa menjadi benteng kedaulatan bangsa di semesta! (Tekan SPASI / Klik)]
wait (0.5) seconds
wait until <<key [space v] pressed?> or <mouse down?>>
start sound [sfx_click v]
say []
hide`
    },
    {
        name: 'hud_hearts_stack1',
        code: `when flag clicked
hide`
    },
    {
        name: 'hud_hearts_stack2',
        code: `when I receive [Start_Babak1 v]
go to [front v] layer
go to x: (-180) y: (155)
show
forever
  if <<(GameState) = [Babak1]> or <<(GameState) = [Babak2]> or <<(GameState) = [Babak3]> or <(GameState) = [Babak4]>>>> then
    show
    if <(Lives) = (3)> then
      switch costume to [3_hati v]
    else
      if <(Lives) = (2)> then
        switch costume to [2_hati v]
      else
        if <(Lives) = (1)> then
          switch costume to [1_hati v]
        else
          switch costume to [0_hati v]
          broadcast [Trigger_Game_Over v]
        end
      end
    end
  else
    hide
  end
end`
    },
    {
        name: 'victory_stack1',
        code: `when flag clicked
hide`
    },
    {
        name: 'victory_stack2',
        code: `when I receive [Show_Victory_Screen v]
go to [front v] layer
go to x: (0) y: (0)
switch costume to [bg_pesan_menang v]
show
say [SELAMAT SATRIA MUDA! Kamu telah menjaga kedaulatan Indonesia dari masa lalu hingga masa depan. Teruslah berkarya untuk bangsa!] for (8) seconds`
    }
];

async function generateAll() {
    console.log('Generating', blocks.length, 'Scratch puzzle blocks...');
    for (const b of blocks) {
        await renderBlockToFiles(b.code, b.name, outDir);
    }
    console.log('All blocks successfully generated in:', outDir);
}

generateAll();
