/* City Pixel — Phaser 3 + Django REST (clean build) */

// ===== CSRF util =====
function getCookie(name){
  let v=null; if(document.cookie && document.cookie!==''){
    const cs=document.cookie.split(';'); for(let c of cs){ c=c.trim();
      if(c.startsWith(name+'=')){ v=decodeURIComponent(c.substring(name.length+1)); break; }
    }
  } return v;
}
const CSRFTOKEN = getCookie('csrftoken');

// ===== Dialogue panel =====
const dlg = document.getElementById('dialogue');
const dlgText = document.getElementById('dialogue-text');
const dlgClose = document.getElementById('dialogue-close');
if (dlgClose) dlgClose.onclick = () => dlg.classList.add('hidden');
document.addEventListener('keydown', e => { if (e.key==='Escape') dlg.classList.add('hidden'); });

// ===== Board (announcement) =====
const board = document.getElementById('board');
const postList = document.getElementById('post-list');
const postForm = document.getElementById('post-form');
const postTitle = document.getElementById('post-title');
const postBody = document.getElementById('post-body');
const postTip = document.getElementById('post-tip');

function escapeHtml(s){ return s.replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m])); }

async function loadPosts(){
  if(!postList) return;
  postList.innerHTML = 'กำลังโหลด...';
  const r = await fetch('/api/posts/');
  const data = await r.json();
  postList.innerHTML = '';
  data.forEach(p=>{
    const el = document.createElement('div'); el.className='post';
    el.innerHTML = `
      <div class="meta">#${p.id} • โดย ${p.author_name ?? 'ไม่ระบุ'} • ${new Date(p.created_at).toLocaleString()}</div>
      <div class="title"><b>${escapeHtml(p.title)}</b></div>
      <div class="body">${escapeHtml(p.body)}</div>
      <div class="comments">
        ${(p.comments||[]).map(c=>`
          <div class="comment">
            <div class="meta">${c.author_name ?? 'ไม่ระบุ'} • ${new Date(c.created_at).toLocaleString()}</div>
            <div>${escapeHtml(c.body)}</div>
          </div>`).join('')}
      </div>
      ${window.USER_IS_AUTH ? `
      <form class="comment-form" data-post="${p.id}">
        <input name="body" placeholder="แสดงความคิดเห็น..." required />
        <button type="submit">ส่ง</button>
      </form>` : `<small>ต้องล็อกอินเพื่อคอมเมนต์</small>`}
    `;
    postList.appendChild(el);
    const cf = el.querySelector('.comment-form');
    if (cf){
      cf.addEventListener('submit', async (e)=>{
        e.preventDefault();
        const body = cf.querySelector('input[name=body]').value.trim();
        if(!body) return;
        await fetch('/api/comments/', {
          method:'POST',
          headers:{'Content-Type':'application/json','X-CSRFToken':CSRFTOKEN},
          body: JSON.stringify({ post: Number(cf.dataset.post), body })
        });
        await loadPosts();
      });
    }
  });
}

if (postForm){
  postForm.addEventListener('submit', async (e)=>{
    e.preventDefault();
    if (!window.USER_IS_AUTH){ postTip.textContent = 'โปรดล็อกอินก่อนโพสต์'; return; }
    postForm.querySelector('button').disabled = true;
    await fetch('/api/posts/', {
      method:'POST',
      headers:{'Content-Type':'application/json','X-CSRFToken':CSRFTOKEN},
      body: JSON.stringify({ title: postTitle.value.trim(), body: postBody.value.trim() })
    });
    postTitle.value=''; postBody.value='';
    postForm.querySelector('button').disabled=false;
    await loadPosts();
  });
}

// ===== Phaser game =====
const TILE=16, WIDTH=800, HEIGHT=600;
const npcs=[ {x:200,y:200,text:'สวัสดี! เมืองเรามีบอร์ดประกาศ กด B เพื่อเปิด'},
             {x:500,y:300,text:'กด E เพื่อคุย / Esc เพื่อปิดกล่องข้อความ'} ];

class CityScene extends Phaser.Scene{
  constructor(){ super('city'); }
  preload(){
    // ใช้สไปรต์ชีตที่เราสร้าง: 32x32, index mapping:
    // down:0..2, left:3..5, right:6..8, up:9..11
    this.load.spritesheet('player','/static/game/assets/player.png',
      { frameWidth:32, frameHeight:32 });
  }
  create(){
    // พื้นหลัง checkerboard
    const g=this.add.graphics();
    for(let y=0;y<HEIGHT;y+=TILE){
      for(let x=0;x<WIDTH;x+=TILE){
        g.fillStyle(((x/TILE+y/TILE)%2===0)?0x1a2636:0x1c2b3f,1);
        g.fillRect(x,y,TILE,TILE);
      }
    }

    this.player = this.physics.add.sprite(120,100,'player',0);
    this.player.setCollideWorldBounds(true);

    // อนิเมชันเดิน 4 ทิศ
    this.anims.create({ key:'down',
      frames:this.anims.generateFrameNumbers('player',{start:0,end:2}), frameRate:10, repeat:-1 });
    this.anims.create({ key:'left',
      frames:this.anims.generateFrameNumbers('player',{start:3,end:5}), frameRate:10, repeat:-1 });
    this.anims.create({ key:'right',
      frames:this.anims.generateFrameNumbers('player',{start:6,end:8}), frameRate:10, repeat:-1 });
    this.anims.create({ key:'up',
      frames:this.anims.generateFrameNumbers('player',{start:9,end:11}), frameRate:10, repeat:-1 });

    // NPCs (จุดสีส้ม)
    this.npcGroup=this.physics.add.staticGroup();
    npcs.forEach(n=>{
      const r=this.add.rectangle(n.x,n.y,14,14,0xf59e0b); this.physics.add.existing(r); r.body.setImmovable(true);
      r.setData('dialog',n.text); this.npcGroup.add(r);
    });

    // คีย์
    this.cursors=this.input.keyboard.createCursorKeys();
    this.keyE=this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.E);

    // คุยกับ NPC
    this.physics.add.overlap(this.player, this.npcGroup, (p,npc)=>{
      if(Phaser.Input.Keyboard.JustDown(this.keyE)){
        dlgText.textContent = npc.getData('dialog');
        dlg.classList.remove('hidden');
      }
    });

    // ปุ่ม B เปิด/ปิดบอร์ด
    this.input.keyboard.on('keydown-B', async ()=>{
      if(board.classList.co
