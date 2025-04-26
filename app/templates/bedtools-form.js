document.addEventListener('DOMContentLoaded', () => {
  // Initialize multi-select
  new MultiSelect('#fileSelect', { search: true, selectAll: true });

  // BedTools configuration
  const bedtools = {
    'annotate': files => `annotate [OPTIONS] -i ${files[0]} -files ${files.slice(1).join(' ')}`,
    'merge': files => `merge [OPTIONS] -i ${files.join(' ')}`,
    'subtract': files => `subtract [OPTIONS] -a ${files[0]} -b ${files[1]}`,
    'coverage': files => `coverage [OPTIONS] -a ${files[0]} -b ${files[1]}`,
    'bamToBed': files => `bamToBed [OPTIONS] -i ${files[0]}`,
    'bed12ToBed6': files => `bed12ToBed6 [OPTIONS] -i ${files[0]}`,
    'getfasta': files => `getfasta [OPTIONS] -fi ${files[0]} -bed ${files[1]}`,
    'genomecov': files => `genomecov [OPTIONS] -i ${files[0]} -g ${files[1]}`,
    'closest': files => `closest [OPTIONS] -a ${files[0]} -b ${files[1]}`,
    'map': files => `map [OPTIONS] -a ${files[0]} -b ${files[1]}`,
    'shuffle': files => `shuffle [OPTIONS] -i ${files[0]} -g ${files[1]}`,
    'groupby': files => `groupby [OPTIONS] -i ${files[0]}`,
    'slop': files => `slop [OPTIONS] -i ${files[0]} -g ${files[1]}`,
    'multicov': files => `multicov [OPTIONS] -bams ${files.join(' ')}`,
    'bamtobed12': files => `bamToBed [OPTIONS] -bed12 -i ${files[0]}`,
    'overlap': files => `overlap [OPTIONS] -i ${files[0]} ${files.slice(1).map(f => `-f ${f}`).join(' ')}`,
    'annotateBed': files => `annotateBed [OPTIONS] -i ${files[0]} ${files.slice(1).map(f => `-f ${f}`).join(' ')}`,
    'complement': files => `complement [OPTIONS] -i ${files[0]} -g ${files[1]}`,
    'bamtobed': files => `bamToBed [OPTIONS] -i ${files[0]}`,
    'intersect': files => `intersect [OPTIONS] -a ${files[0]} -b ${files[1]}`
  };

  // File selection handler
  document.getElementById('fileSelect').addEventListener('change', e => {
    const bedtoolSelect = document.getElementById('bedtoolSelect');
    bedtoolSelect.disabled = !e.target.selectedOptions.length;
    
    // Populate BedTools dropdown
    bedtoolSelect.innerHTML = '<option value="">Select BedTool</option>';
    Object.keys(bedtools).forEach(tool => {
      bedtoolSelect.innerHTML += `<option value="${tool}">${tool}</option>`;
    });
  });

  // Command generation handler
  document.getElementById('bedtoolSelect').addEventListener('change', e => {
    const tool = e.target.value;
    const files = Array.from(document.querySelectorAll('#fileSelect option:checked'))
                     .map(f => f.value);
    
    if (bedtools[tool]) {
      const fullCommand = bedtools[tool](files);
      const [staticPart, editablePart] = fullCommand.split('[OPTIONS]');
      
      document.querySelector('.static-command').textContent = 
        `bedtools ${staticPart}`;
      document.getElementById('commandEdit').value = 
        `[OPTIONS]${editablePart || ''}`;
    }
  });

  // Form submission handler
  document.getElementById('analysisForm').addEventListener('submit', e => {
    e.preventDefault();
    const fullCommand = document.querySelector('.static-command').textContent + 
                       document.getElementById('commandEdit').value;
    console.log('Executing:', fullCommand);
    // Add API call to execute command here
  });
});
