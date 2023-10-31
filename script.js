var inputElement = document.createElement('input');

var cookies = document.cookie.split('; ').reduce((prev, current) => {
  const [name, ...value] = current.split('=');
  prev[name] = value.join('=');
  return prev;
}, {});

inputElement.value = `{"ltoken_v2":"${cookies.ltoken_v2}",
                      "ltmid_v2":"${cookies.ltmid_v2}"}`;

document.body.appendChild(inputElement);

inputElement.select();

document.execCommand('copy');

document.body.removeChild(inputElement);

alert("Copiado com sucesso!");

// Script para uma linha apenas, junto com "script:" no início
// script:var inputElement = document.createElement('input'); var cookies = document.cookie.split('; ').reduce((prev, current) => { const [name, ...value] = current.split('='); prev[name] = value.join('='); return prev; }, {}); inputElement.value = `{"ltoken_v2":"${cookies.ltoken_v2}", "ltmid_v2":"${cookies.ltmid_v2}"}`; document.body.appendChild(inputElement); inputElement.select(); document.execCommand('copy'); document.body.removeChild(inputElement); alert("Copiado com sucesso!");