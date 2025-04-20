document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for navigation links
    document.querySelectorAll('.help-nav a').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                // Update active state
                document.querySelectorAll('.help-nav a').forEach(a => a.classList.remove('active'));
                this.classList.add('active');
                
                // Scroll to target
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Update active state based on scroll position
    const sections = document.querySelectorAll('.help-section');
    const navLinks = document.querySelectorAll('.help-nav a');
    
    window.addEventListener('scroll', function() {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            
            if (pageYOffset >= sectionTop - 60) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });

    // Add copy button functionality for code blocks
    document.querySelectorAll('code').forEach(codeBlock => {
        const copyButton = document.createElement('button');
        copyButton.className = 'btn btn-sm btn-outline-secondary copy-button';
        copyButton.innerHTML = '<i class="fas fa-copy"></i>';
        copyButton.style.position = 'absolute';
        copyButton.style.right = '0';
        copyButton.style.top = '0';
        
        const codeContainer = document.createElement('div');
        codeContainer.style.position = 'relative';
        codeContainer.style.padding = '1rem';
        codeContainer.style.backgroundColor = '#f8f9fa';
        codeContainer.style.borderRadius = '0.5rem';
        codeContainer.style.margin = '1rem 0';
        
        codeBlock.parentNode.insertBefore(codeContainer, codeBlock);
        codeContainer.appendChild(codeBlock);
        codeContainer.appendChild(copyButton);
        
        copyButton.addEventListener('click', function() {
            const text = codeBlock.textContent;
            navigator.clipboard.writeText(text).then(() => {
                const originalText = copyButton.innerHTML;
                copyButton.innerHTML = '<i class="fas fa-check"></i>';
                setTimeout(() => {
                    copyButton.innerHTML = originalText;
                }, 2000);
            });
        });
    });
}); 