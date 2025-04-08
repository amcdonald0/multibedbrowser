document.getElementById('bedtool').addEventListener('change', function() {
    const container = document.getElementById('bedtool-options');
    container.innerHTML = ''; // Clear previous inputs

    const tool = this.value;

    if (tool === 'annotate') {
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
    } if (tool === 'annotate') {
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
    }if (tool === 'annotate') {
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
    }if (tool === 'annotate') {
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
    }if (tool === 'annotate') {
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
    }if (tool === 'annotate') {
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
    }if (tool === 'annotate') {
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
    }if (tool === 'annotate') {
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
    }if (tool === 'annotate') {
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
    }if (tool === 'annotate') {
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
    }else if (tool === 'intersect' || tool === 'coverage') {
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
    }
});
