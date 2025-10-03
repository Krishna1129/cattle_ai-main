document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('fileInput');
    const previewSection = document.getElementById('preview-section');
    const previewImage = document.getElementById('preview-image');
    const loading = document.getElementById('loading');
    const resultsContainer = document.getElementById('results-container');
    const analyzeBtn = document.getElementById('analyze-btn');
    const analyzeStructureBtn = document.getElementById('analyze-structure-btn');

    // Check if all required elements exist
    if (!dropArea || !fileInput || !previewSection || !previewImage) {
        console.error('Required elements not found in DOM');
        return;
    }

    console.log('UI initialized successfully');

    let currentImageFile = null;

    // File upload handling
    dropArea.addEventListener('click', () => fileInput.click());
    dropArea.addEventListener('dragover', handleDragOver);
    dropArea.addEventListener('drop', handleDrop);
    fileInput.addEventListener('change', handleFileSelect);

    // Analysis button handlers
    const comprehensiveBtn = document.getElementById('comprehensive-analysis-btn');
    const demoBtn = document.getElementById('demo-btn');
    const demoNoneBtn = document.getElementById('demo-none-btn');
    
    if (comprehensiveBtn) {
        comprehensiveBtn.addEventListener('click', performComprehensiveAnalysis);
    }
    
    if (demoBtn) {
        demoBtn.addEventListener('click', showDemoResults);
    }
    
    if (demoNoneBtn) {
        demoNoneBtn.addEventListener('click', showDemoNoneResults);
    }
    
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', performClassification);
    }
    
    if (analyzeStructureBtn) {
        analyzeStructureBtn.addEventListener('click', performStructureAnalysis);
    }

    function handleDragOver(e) {
        e.preventDefault();
        dropArea.style.borderColor = 'var(--primary-color)';
        dropArea.style.background = 'var(--bg-primary)';
    }

    function handleDrop(e) {
        e.preventDefault();
        dropArea.style.borderColor = 'var(--border-color)';
        dropArea.style.background = 'var(--bg-secondary)';
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    }

    function handleFileSelect(e) {
        const files = e.target.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    }

    function handleFile(file) {
        if (!file.type.startsWith('image/')) {
            alert('Please select an image file');
            return;
        }

        if (file.size > 10 * 1024 * 1024) {
            alert('File size must be less than 10MB');
            return;
        }

        currentImageFile = file;
        
        // Show preview
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImage.src = e.target.result;
            previewSection.classList.remove('d-none');
            
            // Hide results if showing
            if (resultsContainer) {
                resultsContainer.classList.add('d-none');
            }
        };
        reader.readAsDataURL(file);
    }

    function performClassification() {
        if (!currentImageFile) {
            alert('Please select an image first');
            return;
        }

        showLoading('Analyzing cattle breed...');

        const formData = new FormData();
        formData.append('file', currentImageFile);

        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            hideLoading();
            if (data.success !== false) {
                displayClassificationResults(data);
                showResults();
            } else {
                alert('Error: ' + (data.error || 'Classification failed'));
            }
        })
        .catch(error => {
            hideLoading();
            alert('Error: ' + error.message);
        });
    }

    function performStructureAnalysis() {
        if (!currentImageFile) {
            alert('Please select an image first');
            return;
        }

        showLoading('Analyzing body structure...');

        const formData = new FormData();
        formData.append('file', currentImageFile);

        fetch('/analyze_structure', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            hideLoading();
            if (data.success) {
                // Check if animal type is "None"
                if (data.cattle_type === 'None') {
                    // Only display classification results, no structure analysis
                    displayClassificationResults(data);
                    showResults();
                    
                    // Show informative message
                    const notification = document.createElement('div');
                    notification.className = 'alert alert-info mt-3';
                    notification.innerHTML = `
                        <i class="fas fa-info-circle"></i> 
                        <strong>No Animal Detected:</strong> ${data.message || 'The image does not contain a detectable cattle or buffalo. Body structure analysis is not applicable.'}
                    `;
                    resultsContainer.appendChild(notification);
                } else {
                    // Normal structure analysis results
                    displayStructureResults(data);
                    showResults();
                }
            } else {
                alert('Error: ' + (data.error || 'Structure analysis failed'));
            }
        })
        .catch(error => {
            hideLoading();
            alert('Error: ' + error.message);
        });
    }

    function performComprehensiveAnalysis() {
        if (!currentImageFile) {
            alert('Please select an image first');
            return;
        }

        showLoading('Performing comprehensive analysis...');
        
        // Reset all displays
        resetAllDisplays();

        const formData = new FormData();
        formData.append('file', currentImageFile);

        // First perform classification
        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(classificationData => {
            if (classificationData.success !== false) {
                displayClassificationResults(classificationData);
                
                // Only perform structure analysis if animal type is not "None"
                if (classificationData.cattle_type !== 'None') {
                    const formData2 = new FormData();
                    formData2.append('file', currentImageFile);
                    
                    return fetch('/analyze_structure', {
                        method: 'POST',
                        body: formData2
                    });
                } else {
                    console.log('Skipping structure analysis - animal type is None');
                    hideLoading();
                    showResults();
                    
                    // Show informative message for comprehensive analysis with "None" result
                    const notification = document.createElement('div');
                    notification.className = 'alert alert-info mt-3';
                    notification.innerHTML = `
                        <i class="fas fa-info-circle"></i> 
                        <strong>No Animal Detected:</strong> The image does not contain a detectable cattle or buffalo. Only classification results are shown.
                    `;
                    resultsContainer.appendChild(notification);
                    
                    return Promise.resolve({ success: false, skip: true });
                }
            } else {
                throw new Error(classificationData.error || 'Classification failed');
            }
        })
        .then(response => {
            if (response.skip) {
                // Structure analysis was skipped
                return Promise.resolve({ success: false, skip: true });
            }
            return response.json();
        })
        .then(structureData => {
            if (structureData.skip) {
                // Analysis was skipped, nothing more to do
                console.log('Comprehensive analysis completed (structure analysis skipped)');
                return;
            }
            
            hideLoading();
            if (structureData.success) {
                displayStructureResults(structureData);
                showResults();
                console.log('Comprehensive analysis completed successfully');
            } else {
                alert('Error in structure analysis: ' + (structureData.error || 'Structure analysis failed'));
                showResults(); // Still show classification results
            }
        })
        .catch(error => {
            hideLoading();
            alert('Error: ' + error.message);
            console.error('Comprehensive analysis error:', error);
        });
    }
    
    function resetAllDisplays() {
        // Reset classification displays
        const cattleTypeEl = document.getElementById('cattle-type');
        const breedNameEl = document.getElementById('breed-name');
        if (cattleTypeEl) cattleTypeEl.textContent = '-';
        if (breedNameEl) breedNameEl.textContent = '-';
        
        // Reset parameter displays
        const parameterIds = ['body-condition-score', 'body-length', 'chest-depth', 'chest-width', 'height-withers', 'rump-angle'];
        parameterIds.forEach(id => {
            const el = document.getElementById(id);
            if (el) el.textContent = '-';
        });
        
        // Reset ATC score
        const atcScoreEl = document.getElementById('atc-score-value');
        const atcLevelEl = document.getElementById('atc-level');
        if (atcScoreEl) atcScoreEl.textContent = '0';
        if (atcLevelEl) atcLevelEl.textContent = 'Calculating...';
        
        // Show body parameters and ATC sections by default (they will be hidden if needed)
        const bodyParametersSection = document.querySelector('.body-parameters-section');
        const atcScoreSection = document.querySelector('.atc-score-section');
        if (bodyParametersSection) {
            bodyParametersSection.style.display = 'block';
        }
        if (atcScoreSection) {
            atcScoreSection.style.display = 'block';
        }
    }

    function showLoading(message = 'Processing...') {
        const loadingContent = loading.querySelector('.loading-content p');
        if (loadingContent) {
            loadingContent.textContent = message;
        }
        
        if (loading) {
            loading.classList.remove('d-none');
        }
        if (resultsContainer) {
            resultsContainer.classList.add('d-none');
        }
    }

    function hideLoading() {
        if (loading) {
            loading.classList.add('d-none');
        }
    }

    function showResults() {
        if (resultsContainer) {
            resultsContainer.classList.remove('d-none');
            resultsContainer.scrollIntoView({ behavior: 'smooth' });
        }
    }

    function displayClassificationResults(data) {
        console.log('Classification data received:', data);
        
        // Update cattle type
        const cattleTypeEl = document.getElementById('cattle-type');
        const cattleConfidenceEl = document.getElementById('cattle-confidence');
        const cattlePercentageEl = document.getElementById('cattle-percentage');
        
        if (cattleTypeEl && data.cattle_type) {
            cattleTypeEl.textContent = data.cattle_type;
            console.log('Updated cattle type:', data.cattle_type);
        }
        
        if (cattleConfidenceEl && cattlePercentageEl && data.cattle_confidence) {
            const confidence = parseFloat(data.cattle_confidence.replace('%', ''));
            cattleConfidenceEl.style.width = confidence + '%';
            cattlePercentageEl.textContent = data.cattle_confidence;
            console.log('Updated cattle confidence:', data.cattle_confidence);
            
            // Update confidence color based on value
            if (confidence >= 80) {
                cattleConfidenceEl.style.background = 'var(--success-color)';
            } else if (confidence >= 60) {
                cattleConfidenceEl.style.background = 'var(--warning-color)';
            } else {
                cattleConfidenceEl.style.background = 'var(--error-color)';
            }
        }

        // Update breed information
        const breedCard = document.getElementById('breed-card');
        const breedNameEl = document.getElementById('breed-name');
        const breedConfidenceEl = document.getElementById('breed-confidence');
        const breedPercentageEl = document.getElementById('breed-percentage');
        
        console.log('Breed data:', { breed: data.breed, confidence: data.breed_confidence });
        
        if (data.breed && data.breed !== 'Unknown' && breedCard) {
            breedCard.style.display = 'block';
            console.log('Showing breed card for:', data.breed);
            
            if (breedNameEl) {
                breedNameEl.textContent = data.breed;
            }
            
            if (breedConfidenceEl && breedPercentageEl && data.breed_confidence) {
                const breedConf = parseFloat(data.breed_confidence.replace('%', ''));
                breedConfidenceEl.style.width = breedConf + '%';
                breedPercentageEl.textContent = data.breed_confidence;
                console.log('Updated breed confidence:', data.breed_confidence);
                
                // Update confidence color
                if (breedConf >= 80) {
                    breedConfidenceEl.style.background = 'var(--success-color)';
                } else if (breedConf >= 60) {
                    breedConfidenceEl.style.background = 'var(--warning-color)';
                } else {
                    breedConfidenceEl.style.background = 'var(--error-color)';
                }
            }
        } else {
            console.log('Hiding breed card - no breed data or unknown breed');
            if (breedCard) {
                breedCard.style.display = 'none';
            }
        }

        // Hide body parameters and ATC sections if animal type is "None"
        const bodyParametersSection = document.querySelector('.body-parameters-section');
        const atcScoreSection = document.querySelector('.atc-score-section');
        const reportSection = document.querySelector('.report-section');
        
        if (data.cattle_type === 'None') {
            console.log('Animal type is None - hiding body parameters, ATC sections, and analysis report');
            if (bodyParametersSection) {
                bodyParametersSection.style.display = 'none';
            }
            if (atcScoreSection) {
                atcScoreSection.style.display = 'none';
            }
            if (reportSection) {
                reportSection.style.display = 'none';
            }
        } else {
            console.log('Animal type is valid - showing body parameters, ATC sections, and analysis report');
            if (bodyParametersSection) {
                bodyParametersSection.style.display = 'block';
            }
            if (atcScoreSection) {
                atcScoreSection.style.display = 'block';
            }
            if (reportSection) {
                reportSection.style.display = 'block';
            }
        }
    }

    function displayStructureResults(data) {
        // Display analysis image
        const structureImage = document.getElementById('structure-image');
        if (structureImage && data.visualization) {
            structureImage.src = 'data:image/jpeg;base64,' + data.visualization;
        }

        // Display body parameters
        if (data.measurements) {
            updateParameter('body-condition-score', data.measurements.body_condition_score, '/5.0', 'Score');
            updateParameter('body-length', data.measurements.body_length, 'meters', 'Length');
            updateParameter('chest-depth', data.measurements.chest_depth, 'meters', 'Depth');
            updateParameter('chest-width', data.measurements.chest_width, 'meters', 'Width');
            updateParameter('height-withers', data.measurements.height_at_withers, 'meters', 'Height');
            updateParameter('rump-angle', data.measurements.rump_angle, 'degrees', 'Angle');
        }

        // Display ATC score
        if (data.atc_score) {
            displayATCScore(data.atc_score);
        }

        // Display report
        const reportContent = document.getElementById('analysis-report');
        if (reportContent && data.report) {
            reportContent.textContent = data.report;
        }

        // Also display classification if available
        if (data.cattle_type) {
            displayClassificationResults(data);
        }
    }

    function showDemoResults() {
        // Show demo results to demonstrate all features
        resetAllDisplays();
        
        // Demo classification results
        const demoClassificationData = {
            cattle_type: "Cow",
            cattle_confidence: "92%",
            breed: "Holstein Friesian",
            breed_confidence: "87%",
            success: true
        };
        
        // Demo structure results
        const demoStructureData = {
            success: true,
            measurements: {
                body_condition_score: 3.8,
                body_length: 1.85,
                chest_depth: 0.78,
                chest_width: 0.65,
                height_at_withers: 1.45,
                rump_angle: 12
            },
            atc_score: {
                overall_score: 78,
                level: "Good",
                components: {
                    "Morphometric Accuracy": 82,
                    "Classification Confidence": 75,
                    "Body Structure Quality": 80
                },
                recommendations: [
                    "High classification confidence indicates clear breed characteristics",
                    "Body structure measurements are within normal ranges",
                    "Consider additional angles for comprehensive analysis"
                ]
            }
        };
        
        // Display the demo results
        displayClassificationResults(demoClassificationData);
        displayStructureResults(demoStructureData);
        showResults();
        
        // Show a notification
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--success-color);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 0.5rem;
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        `;
        notification.innerHTML = '<i class="fas fa-info-circle"></i> Demo results displayed - showing all features!';
        document.body.appendChild(notification);
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 4000);
    }

    function showDemoNoneResults() {
        // Show demo results for "None" detection (no cattle/buffalo detected)
        resetAllDisplays();
        
        // Demo classification results for "None"
        const demoNoneData = {
            cattle_type: "None",
            cattle_confidence: "85%",
            success: true
        };
        
        // Display the demo results (body parameters and ATC will be hidden automatically)
        displayClassificationResults(demoNoneData);
        showResults();
        
        // Show a notification
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--error-color);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 0.5rem;
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        `;
        notification.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Demo "None" detection - body analysis sections hidden!';
        document.body.appendChild(notification);
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 4000);
    }

    function updateParameter(elementId, value, unit, type) {
        const valueEl = document.getElementById(elementId);
        const statusEl = document.getElementById(elementId.replace(elementId.split('-').pop(), 'status'));
        
        if (valueEl && value !== undefined && value !== null) {
            // Format value based on type
            let formattedValue;
            if (type === 'Score') {
                formattedValue = value.toFixed(1);
            } else if (type === 'Angle') {
                formattedValue = value.toFixed(0);
            } else {
                formattedValue = value.toFixed(2);
            }
            
            valueEl.textContent = formattedValue;
            
            // Update status based on value quality
            if (statusEl) {
                let status = 'Normal';
                let statusClass = 'good';
                
                if (type === 'Score') {
                    if (value >= 4.0) {
                        status = 'Excellent';
                        statusClass = 'excellent';
                    } else if (value >= 3.0) {
                        status = 'Good';
                        statusClass = 'good';
                    } else if (value >= 2.0) {
                        status = 'Fair';
                        statusClass = 'fair';
                    } else {
                        status = 'Poor';
                        statusClass = 'poor';
                    }
                }
                
                statusEl.textContent = status;
                statusEl.className = `parameter-status ${statusClass}`;
            }
        } else if (valueEl) {
            valueEl.textContent = '-';
            if (statusEl) {
                statusEl.textContent = 'Not available';
                statusEl.className = 'parameter-status';
            }
        }
    }

    function displayATCScore(atcData) {
        // Update main score
        const scoreValueEl = document.getElementById('atc-score-value');
        const levelEl = document.getElementById('atc-level');
        
        if (scoreValueEl && atcData.atc_score !== undefined) {
            scoreValueEl.textContent = Math.round(atcData.atc_score);
            
            // Update circle color based on score
            const circle = scoreValueEl.closest('.atc-score-circle');
            const mainCard = scoreValueEl.closest('.atc-main-card');
            
            if (circle && mainCard) {
                let levelClass = 'good';
                if (atcData.atc_score >= 85) {
                    levelClass = 'excellent';
                    circle.style.background = 'var(--success-color)';
                } else if (atcData.atc_score >= 70) {
                    levelClass = 'good';
                    circle.style.background = 'var(--primary-gradient)';
                } else if (atcData.atc_score >= 55) {
                    levelClass = 'fair';
                    circle.style.background = 'var(--warning-color)';
                } else {
                    levelClass = 'poor';
                    circle.style.background = 'var(--error-color)';
                }
                
                mainCard.className = `atc-main-card ${levelClass}`;
            }
        }
        
        if (levelEl && atcData.confidence_level) {
            levelEl.textContent = atcData.confidence_level;
        }

        // Update components
        const componentsContainer = document.getElementById('atc-components');
        if (componentsContainer && atcData.components) {
            componentsContainer.innerHTML = '';
            
            Object.entries(atcData.components).forEach(([component, score]) => {
                const componentEl = document.createElement('div');
                componentEl.className = 'component-item';
                
                const componentName = component.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                
                componentEl.innerHTML = `
                    <span class="component-name">${componentName}</span>
                    <span class="component-score">${score}%</span>
                    <div class="component-progress">
                        <div class="component-fill" style="width: ${score}%; background: ${getComponentColor(score)}"></div>
                    </div>
                `;
                
                componentsContainer.appendChild(componentEl);
            });
        }

        // Update recommendations
        const recommendationsContainer = document.getElementById('atc-recommendations');
        if (recommendationsContainer && atcData.recommendations) {
            recommendationsContainer.innerHTML = '';
            
            atcData.recommendations.forEach(recommendation => {
                const recEl = document.createElement('div');
                recEl.className = 'recommendation-item';
                recEl.textContent = recommendation;
                recommendationsContainer.appendChild(recEl);
            });
        }
    }

    function getComponentColor(score) {
        if (score >= 85) return 'var(--success-color)';
        if (score >= 70) return 'var(--primary-color)';
        if (score >= 55) return 'var(--warning-color)';
        return 'var(--error-color)';
    }

    // Initialize UI state
    if (resultsContainer) {
        resultsContainer.classList.add('d-none');
    }
    if (loading) {
        loading.classList.add('d-none');
    }
    if (previewSection) {
        previewSection.classList.add('d-none');
    }
});