async function q(path){return fetch(path).then(r=>r.json())}
const log = msg => document.getElementById('log').textContent += '\n' + msg

async function init(){
  const s = await q('/api/states/')
  const stateSel = document.getElementById('state')
  s.states.forEach(st => {
    const o = document.createElement('option'); o.value = st; o.textContent = st; stateSel.appendChild(o)
  })
  document.getElementById('download').addEventListener('click', async ()=>{
    const payload = new FormData()
    payload.append('state', document.getElementById('state').value)
    payload.append('district', document.getElementById('district').value)
    payload.append('complex', document.getElementById('complex').value)
    payload.append('court', document.getElementById('court').value)
    payload.append('date', document.getElementById('date').value)
    const res = await fetch('/api/download/', {method:'POST', body: payload})
    const j = await res.json()
    if(!j.ok){
      log('Download blocked: ' + j.message)
      log('Hint: open scripts/download_causelist.py to run a browser automation that lets you complete the captcha once.')
    } else {
      log('Download started...')
    }
  })
}
window.addEventListener('load', init)
