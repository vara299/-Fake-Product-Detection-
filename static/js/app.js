// Sample product cards (images are placeholders)
const sampleProducts = [
  { title: 'Luxury Watch', img: '/static/sample_images/genuine_sample.jpg', id: 'watch1' },
  { title: 'Designer Bag', img: '/static/sample_images/fake_sample.jpg', id: 'bag1' },
  { title: 'Sneakers', img: '/static/sample_images/genuine_sample.jpg', id: 'shoe1' },
  { title: 'Smartphone', img: '/static/sample_images/fake_sample.jpg', id: 'phone1' }
];

function buildCards(){
  const container = document.getElementById('cards');
  sampleProducts.forEach(p=>{
    const div = document.createElement('div');
    div.className = 'card';
    div.innerHTML = `<img src="${p.img}" alt=""><div class="title">${p.title}</div>`;
    container.appendChild(div);
  });
}
buildCards();

const uploadInput = document.getElementById('uploadInput');
const uploadBtn = document.getElementById('uploadBtn');
const modal = document.getElementById('resultModal');
const closeModal = document.getElementById('closeModal');
const resultLabel = document.getElementById('resultLabel');
const resultConf = document.getElementById('resultConf');
const resultReason = document.getElementById('resultReason');
const resultImage = document.getElementById('resultImage');

uploadBtn.addEventListener('click', async ()=>{
  const file = uploadInput.files[0];
  if(!file){ alert('Choose an image first'); return; }
  const form = new FormData();
  form.append('image', file);
  uploadBtn.disabled = true;
  uploadBtn.textContent = 'Detecting...';
  try{
    const res = await fetch('/predict', { method: 'POST', body: form });
    const data = await res.json();
    if(data.error){ alert(data.error); return; }
    resultLabel.textContent = data.label;
    resultConf.textContent = `Confidence: ${Math.round(data.confidence*100)}%`;
    resultReason.textContent = `Reason: ${data.reason}`;
    // show uploaded preview
    const url = URL.createObjectURL(file);
    resultImage.src = url;
    modal.classList.remove('hidden');
  }catch(err){
    alert('Error: ' + err.message);
  }finally{
    uploadBtn.disabled = false;
    uploadBtn.textContent = 'Detect Fake';
  }
});

closeModal.addEventListener('click', ()=> modal.classList.add('hidden'));
