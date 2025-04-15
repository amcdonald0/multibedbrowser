document.addEventListener('DOMContentLoaded', function () {
    const bedtoolSelect = document.getElementById('bedtool');
    const container = document.getElementById('bedtool-options');
  
    if (bedtoolSelect && container) {
      bedtoolSelect.addEventListener('change', function () {
        container.innerHTML = ''; // Clear previous inputs
        const tool = this.value;
  
        switch (tool) {
          case 'annotate':
            container.innerHTML = `
              <div class="form-group">
                <label for="input-file">Input File (BED/GFF/VCF)</label>
                <input type="file" class="form-control-file" id="input-file" name="input_file" required>
              </div>
              <div class="form-group">
                <label>Annotation Files</label>
                <input type="file" class="form-control-file mb-2" name="annotation_files[]" multiple required>
                <small class="form-text text-muted">You can select multiple annotation files.</small>
              </div>
            `;
            break;
  
          case 'intersect':
          case 'coverage':
          case 'subtract':
          case 'overlap':
            container.innerHTML = `
              <div class="form-group">
                <label for="fileA">File A (BED)</label>
                <input type="file" class="form-control-file" id="fileA" name="fileA" required>
              </div>
              <div class="form-group">
                <label for="fileB">File B (BED)</label>
                <input type="file" class="form-control-file" id="fileB" name="fileB" required>
              </div>
            `;
            break;
  
          case 'merge':
          case 'sort':
          case 'genomecov':
          case 'slop':
          case 'complement':
            container.innerHTML = `
              <div class="form-group">
                <label for="input-file">Input File (BED)</label>
                <input type="file" class="form-control-file" id="input-file" name="input_file" required>
              </div>
            `;
            break;
  
          case 'closest':
          case 'map':
          case 'groupby':
            container.innerHTML = `
              <div class="form-group">
                <label for="fileA">File A (BED)</label>
                <input type="file" class="form-control-file" id="fileA" name="fileA" required>
              </div>
              <div class="form-group">
                <label for="fileB">File B (BED)</label>
                <input type="file" class="form-control-file" id="fileB" name="fileB" required>
              </div>
            `;
            break;
  
          case 'getfasta':
            container.innerHTML = `
              <div class="form-group">
                <label for="bed-file">BED File</label>
                <input type="file" class="form-control-file" id="bed-file" name="bed_file" required>
              </div>
              <div class="form-group">
                <label for="fasta-file">Reference Genome (FASTA)</label>
                <input type="file" class="form-control-file" id="fasta-file" name="fasta_file" required>
              </div>
            `;
            break;
  
          case 'shuffle':
            container.innerHTML = `
              <div class="form-group">
                <label for="bed-file">Input BED File</label>
                <input type="file" class="form-control-file" id="bed-file" name="bed_file" required>
              </div>
              <div class="form-group">
                <label for="genome-file">Genome File</label>
                <input type="file" class="form-control-file" id="genome-file" name="genome_file" required>
              </div>
            `;
            break;
  
          case 'annotatebed':
          case 'multicov':
            container.innerHTML = `
              <div class="form-group">
                <label>Input BED Files</label>
                <input type="file" class="form-control-file" name="input_bed_files[]" multiple required>
                <small class="form-text text-muted">Select multiple BED files.</small>
              </div>
            `;
            break;
  
          case 'bamtobed':
            container.innerHTML = `
              <div class="form-group">
                <label for="bam-file">Input BAM File</label>
                <input type="file" class="form-control-file" id="bam-file" name="bam_file" required>
              </div>
            `;
            break;
  
          default:
            container.innerHTML = ''; // Clear if no valid tool selected
        }
      });
    }
  });
  