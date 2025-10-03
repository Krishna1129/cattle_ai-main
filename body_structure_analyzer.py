import cv2
import numpy as np
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image, ImageDraw, ImageFont
import math

class BodyStructureAnalyzer:
    """
    Body Structure Analyzer for cattle morphometric measurements
    This class provides methods to extract and quantify body structure parameters
    including ATC (Animal Type Classification) score calculation
    """
    
    def __init__(self):
        self.body_parts_map = {
            'nose': 0, 'left_eye': 1, 'right_eye': 2, 'left_ear': 3, 'right_ear': 4,
            'neck_base': 5, 'withers': 6, 'back_mid': 7, 'rump': 8, 'tail_base': 9,
            'shoulder': 10, 'elbow': 11, 'knee': 12, 'front_hoof': 13,
            'hip': 14, 'stifle': 15, 'hock': 16, 'rear_hoof': 17,
            'chest_front': 18, 'chest_deep': 19, 'belly': 20, 'udder': 21
        }
        
        # Standard cattle measurements (these can be calibrated based on real data)
        self.measurement_ratios = {
            'body_length_to_height': 1.25,  # Average ratio for dairy cattle
            'chest_width_to_height': 0.45,
            'rump_width_to_height': 0.38
        }
        
        # ATC scoring parameters
        self.atc_weights = {
            'body_proportions': 0.25,
            'head_characteristics': 0.20,
            'limb_structure': 0.20,
            'overall_symmetry': 0.15,
            'muscle_definition': 0.10,
            'coat_pattern': 0.10
        }
    
    def detect_keypoints(self, image):
        """
        Detect key body structure points using image processing
        In a production system, this would use a trained keypoint detection model
        For now, we'll use edge detection and contour analysis as a proof of concept
        """
        # Convert PIL to cv2
        img_array = np.array(image)
        if len(img_array.shape) == 3:
            img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        else:
            img_cv = img_array
        
        # Preprocessing
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Edge detection
        edges = cv2.Canny(blurred, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return None
            
        # Find the largest contour (assumed to be the animal)
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Get bounding rectangle
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        # Calculate approximate keypoints based on cattle anatomy
        keypoints = self._estimate_keypoints(x, y, w, h, largest_contour)
        
        return keypoints
    
    def _estimate_keypoints(self, x, y, w, h, contour):
        """
        Estimate keypoints based on typical cattle body proportions
        """
        keypoints = {}
        
        # Basic anatomical proportions for cattle
        # These are approximate and would be refined with actual training data
        keypoints['nose'] = (x + int(w * 0.1), y + int(h * 0.3))
        keypoints['withers'] = (x + int(w * 0.3), y + int(h * 0.2))
        keypoints['rump'] = (x + int(w * 0.8), y + int(h * 0.25))
        keypoints['shoulder'] = (x + int(w * 0.25), y + int(h * 0.4))
        keypoints['hip'] = (x + int(w * 0.75), y + int(h * 0.4))
        keypoints['chest_front'] = (x + int(w * 0.2), y + int(h * 0.5))
        keypoints['chest_deep'] = (x + int(w * 0.4), y + int(h * 0.7))
        keypoints['front_hoof'] = (x + int(w * 0.25), y + int(h * 0.95))
        keypoints['rear_hoof'] = (x + int(w * 0.75), y + int(h * 0.95))
        keypoints['belly'] = (x + int(w * 0.5), y + int(h * 0.8))
        
        return keypoints
    
    def calculate_measurements(self, keypoints, image_width, image_height, reference_scale=1.0):
        """
        Calculate body structure measurements from keypoints
        reference_scale: pixels per meter (for calibration)
        """
        if not keypoints:
            return None
            
        measurements = {}
        
        # Body length (nose to rump)
        if 'nose' in keypoints and 'rump' in keypoints:
            body_length_px = self._distance(keypoints['nose'], keypoints['rump'])
            measurements['body_length'] = body_length_px / reference_scale
        
        # Height at withers
        if 'withers' in keypoints and 'front_hoof' in keypoints:
            height_px = abs(keypoints['withers'][1] - keypoints['front_hoof'][1])
            measurements['height_at_withers'] = height_px / reference_scale
        
        # Chest width (estimated from shoulder points)
        if 'shoulder' in keypoints and 'chest_front' in keypoints:
            chest_width_px = self._distance(keypoints['shoulder'], keypoints['chest_front'])
            measurements['chest_width'] = chest_width_px / reference_scale
        
        # Chest depth
        if 'withers' in keypoints and 'chest_deep' in keypoints:
            chest_depth_px = abs(keypoints['withers'][1] - keypoints['chest_deep'][1])
            measurements['chest_depth'] = chest_depth_px / reference_scale
        
        # Rump angle (approximate)
        if 'withers' in keypoints and 'rump' in keypoints:
            rump_angle = self._calculate_angle(keypoints['withers'], keypoints['rump'])
            measurements['rump_angle'] = rump_angle
        
        # Body condition score estimation based on ratios
        measurements['body_condition_score'] = self._estimate_body_condition(measurements)
        
        return measurements
    
    def calculate_atc_score(self, keypoints, measurements, image, cattle_type=None):
        """
        Calculate ATC (Animal Type Classification) score based on morphometric analysis
        ATC score evaluates the quality and accuracy of animal type classification
        
        Parameters:
        - keypoints: Detected body structure keypoints
        - measurements: Calculated body measurements
        - image: PIL Image object
        - cattle_type: Predicted cattle type ('Cow', 'Buffalo', 'None')
        
        Returns:
        - Dictionary containing ATC score and component scores
        """
        try:
            if not keypoints or not measurements:
                return {
                    'atc_score': 0.0,
                    'confidence_level': 'Low',
                    'components': {
                        'body_proportions': 0.0,
                        'head_characteristics': 0.0,
                        'limb_structure': 0.0,
                        'overall_symmetry': 0.0,
                        'muscle_definition': 0.0,
                        'coat_pattern': 0.0
                    },
                    'recommendations': ['Insufficient data for accurate ATC scoring']
                }
            
            # Calculate component scores
            components = {}
            
            # 1. Body Proportions Score (25%)
            components['body_proportions'] = self._calculate_body_proportion_score(measurements)
            
            # 2. Head Characteristics Score (20%)
            components['head_characteristics'] = self._calculate_head_characteristics_score(keypoints, image)
            
            # 3. Limb Structure Score (20%)
            components['limb_structure'] = self._calculate_limb_structure_score(keypoints, measurements)
            
            # 4. Overall Symmetry Score (15%)
            components['overall_symmetry'] = self._calculate_symmetry_score(keypoints)
            
            # 5. Muscle Definition Score (10%)
            components['muscle_definition'] = self._calculate_muscle_definition_score(image, keypoints)
            
            # 6. Coat Pattern Score (10%)
            components['coat_pattern'] = self._calculate_coat_pattern_score(image)
            
            # Calculate weighted ATC score
            atc_score = sum(
                components[component] * self.atc_weights[component] 
                for component in components
            )
            
            # Normalize to 0-100 scale
            atc_score = min(100.0, max(0.0, atc_score * 100))
            
            # Determine confidence level
            if atc_score >= 85:
                confidence_level = 'Excellent'
            elif atc_score >= 70:
                confidence_level = 'Good'
            elif atc_score >= 55:
                confidence_level = 'Fair'
            else:
                confidence_level = 'Poor'
            
            # Generate recommendations
            recommendations = self._generate_atc_recommendations(components, atc_score)
            
            return {
                'atc_score': round(atc_score, 2),
                'confidence_level': confidence_level,
                'components': {k: round(v * 100, 1) for k, v in components.items()},
                'recommendations': recommendations
            }
            
        except Exception as e:
            return {
                'atc_score': 0.0,
                'confidence_level': 'Error',
                'components': {},
                'recommendations': [f'Error calculating ATC score: {str(e)}']
            }
    
    def _distance(self, point1, point2):
        """Calculate Euclidean distance between two points"""
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    def _calculate_angle(self, point1, point2):
        """Calculate angle between two points relative to horizontal"""
        dx = point2[0] - point1[0]
        dy = point2[1] - point1[1]
        angle = math.degrees(math.atan2(dy, dx))
        return abs(angle)
    
    def _estimate_body_condition(self, measurements):
        """
        Estimate body condition score (1-5 scale) based on measurements
        This is a simplified estimation - real BCS requires visual assessment
        """
        if not measurements or 'chest_depth' not in measurements:
            return None
        
        # Simple heuristic based on chest depth to height ratio
        if 'height_at_withers' in measurements:
            ratio = measurements['chest_depth'] / measurements['height_at_withers']
            if ratio < 0.4:
                return 2.0  # Thin
            elif ratio < 0.5:
                return 3.0  # Moderate
            elif ratio < 0.6:
                return 4.0  # Good
            else:
                return 4.5  # Very good
        
        return 3.0  # Default moderate score
    
    def visualize_measurements(self, image, keypoints, measurements):
        """
        Create a visualization of the measurements on the image
        """
        # Convert to PIL for drawing
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        
        # Create a copy for drawing
        vis_image = image.copy()
        draw = ImageDraw.Draw(vis_image)
        
        # Draw keypoints
        if keypoints:
            for name, point in keypoints.items():
                # Draw point
                radius = 5
                draw.ellipse([point[0]-radius, point[1]-radius, 
                            point[0]+radius, point[1]+radius], 
                           fill='red', outline='white')
                
                # Draw label
                draw.text((point[0]+8, point[1]-8), name, fill='white')
        
        # Draw measurement lines
        if keypoints and measurements:
            # Body length line
            if 'nose' in keypoints and 'rump' in keypoints:
                draw.line([keypoints['nose'], keypoints['rump']], 
                         fill='yellow', width=3)
                
                # Add measurement text
                mid_x = (keypoints['nose'][0] + keypoints['rump'][0]) // 2
                mid_y = (keypoints['nose'][1] + keypoints['rump'][1]) // 2
                draw.text((mid_x, mid_y), 
                         f"Length: {measurements.get('body_length', 0):.1f}m", 
                         fill='yellow')
            
            # Height line
            if 'withers' in keypoints and 'front_hoof' in keypoints:
                draw.line([keypoints['withers'], keypoints['front_hoof']], 
                         fill='green', width=3)
                
                # Add measurement text
                draw.text((keypoints['withers'][0]+10, keypoints['withers'][1]), 
                         f"Height: {measurements.get('height_at_withers', 0):.1f}m", 
                         fill='green')
        
        return vis_image
    
    def generate_report(self, measurements, animal_type, breed):
        """
        Generate a comprehensive body structure analysis report
        """
        if not measurements:
            return "Unable to generate report - no measurements available"
        
        report = f"""
BODY STRUCTURE ANALYSIS REPORT
==============================

Animal Classification:
- Type: {animal_type}
- Breed: {breed}

Morphometric Measurements:
"""
        
        if 'body_length' in measurements:
            report += f"- Body Length: {measurements['body_length']:.2f} meters\n"
        
        if 'height_at_withers' in measurements:
            report += f"- Height at Withers: {measurements['height_at_withers']:.2f} meters\n"
        
        if 'chest_width' in measurements:
            report += f"- Chest Width: {measurements['chest_width']:.2f} meters\n"
        
        if 'chest_depth' in measurements:
            report += f"- Chest Depth: {measurements['chest_depth']:.2f} meters\n"
        
        if 'rump_angle' in measurements:
            report += f"- Rump Angle: {measurements['rump_angle']:.1f} degrees\n"
        
        if 'body_condition_score' in measurements:
            report += f"- Body Condition Score: {measurements['body_condition_score']:.1f}/5.0\n"
        
        # Add interpretation
        report += "\nInterpretation:\n"
        
        if 'body_condition_score' in measurements:
            bcs = measurements['body_condition_score']
            if bcs < 2.5:
                report += "- Body condition is below optimal. Consider nutritional supplementation.\n"
            elif bcs < 3.5:
                report += "- Body condition is moderate. Monitor feeding program.\n"
            elif bcs < 4.2:
                report += "- Body condition is good. Maintain current management.\n"
            else:
                report += "- Body condition is very good. Animal is well-maintained.\n"
        
        if 'body_length' in measurements and 'height_at_withers' in measurements:
            ratio = measurements['body_length'] / measurements['height_at_withers']
            if ratio > 1.3:
                report += "- Body conformation shows good dairy type characteristics.\n"
            elif ratio < 1.2:
                report += "- Body appears more compact - suitable for beef production.\n"
            else:
                report += "- Body conformation is within normal range.\n"
        
        report += "\nNote: Measurements are estimates based on image analysis. "
        report += "For precise measurements, manual measurement is recommended."
        
        return report
    
    def calculate_atc_score(self, keypoints, measurements, image, cattle_type=None):
        """
        Calculate ATC (Animal Type Classification) score based on morphometric analysis
        ATC score evaluates the quality and accuracy of animal type classification
        
        Parameters:
        - keypoints: Detected body structure keypoints
        - measurements: Calculated body measurements
        - image: PIL Image object
        - cattle_type: Predicted cattle type ('Cow', 'Buffalo', 'None')
        
        Returns:
        - Dictionary containing ATC score and component scores
        """
        try:
            if not keypoints or not measurements:
                return {
                    'atc_score': 0.0,
                    'confidence_level': 'Low',
                    'components': {
                        'body_proportions': 0.0,
                        'head_characteristics': 0.0,
                        'limb_structure': 0.0,
                        'overall_symmetry': 0.0,
                        'muscle_definition': 0.0,
                        'coat_pattern': 0.0
                    },
                    'recommendations': ['Insufficient data for accurate ATC scoring']
                }
            
            # ATC scoring weights
            atc_weights = {
                'body_proportions': 0.25,
                'head_characteristics': 0.20,
                'limb_structure': 0.20,
                'overall_symmetry': 0.15,
                'muscle_definition': 0.10,
                'coat_pattern': 0.10
            }
            
            # Calculate component scores
            components = {}
            
            # 1. Body Proportions Score (25%)
            components['body_proportions'] = self._calculate_body_proportion_score(measurements)
            
            # 2. Head Characteristics Score (20%)
            components['head_characteristics'] = self._calculate_head_characteristics_score(keypoints, image)
            
            # 3. Limb Structure Score (20%)
            components['limb_structure'] = self._calculate_limb_structure_score(keypoints, measurements)
            
            # 4. Overall Symmetry Score (15%)
            components['overall_symmetry'] = self._calculate_symmetry_score(keypoints)
            
            # 5. Muscle Definition Score (10%)
            components['muscle_definition'] = self._calculate_muscle_definition_score(image, keypoints)
            
            # 6. Coat Pattern Score (10%)
            components['coat_pattern'] = self._calculate_coat_pattern_score(image)
            
            # Calculate weighted ATC score
            atc_score = sum(
                components[component] * atc_weights[component] 
                for component in components
            )
            
            # Normalize to 0-100 scale
            atc_score = min(100.0, max(0.0, atc_score * 100))
            
            # Determine confidence level
            if atc_score >= 85:
                confidence_level = 'Excellent'
            elif atc_score >= 70:
                confidence_level = 'Good'
            elif atc_score >= 55:
                confidence_level = 'Fair'
            else:
                confidence_level = 'Poor'
            
            # Generate recommendations
            recommendations = self._generate_atc_recommendations(components, atc_score)
            
            return {
                'atc_score': round(atc_score, 2),
                'confidence_level': confidence_level,
                'components': {k: round(v * 100, 1) for k, v in components.items()},
                'recommendations': recommendations
            }
            
        except Exception as e:
            return {
                'atc_score': 0.0,
                'confidence_level': 'Error',
                'components': {},
                'recommendations': [f'Error calculating ATC score: {str(e)}']
            }
    
    def _calculate_body_proportion_score(self, measurements):
        """Calculate body proportion score based on ideal ratios"""
        try:
            score = 0.0
            checks = 0
            
            # Check body length to height ratio
            if 'body_length' in measurements and 'height_at_withers' in measurements:
                if measurements['height_at_withers'] > 0:
                    ratio = measurements['body_length'] / measurements['height_at_withers']
                    ideal_ratio = self.measurement_ratios['body_length_to_height']
                    deviation = abs(ratio - ideal_ratio) / ideal_ratio
                    score += max(0, 1 - deviation)
                    checks += 1
            
            # Check chest proportions
            if 'chest_width' in measurements and 'height_at_withers' in measurements:
                if measurements['height_at_withers'] > 0:
                    ratio = measurements['chest_width'] / measurements['height_at_withers']
                    ideal_ratio = self.measurement_ratios['chest_width_to_height']
                    deviation = abs(ratio - ideal_ratio) / ideal_ratio
                    score += max(0, 1 - deviation)
                    checks += 1
            
            # Check body condition score consistency
            if 'body_condition_score' in measurements:
                bcs = measurements['body_condition_score']
                if 2.5 <= bcs <= 4.5:  # Ideal range
                    score += 1.0
                else:
                    score += 0.5
                checks += 1
            
            return score / max(1, checks)
            
        except Exception:
            return 0.5  # Default moderate score
    
    def _calculate_head_characteristics_score(self, keypoints, image):
        """Calculate head characteristics score"""
        try:
            score = 0.0
            
            # Check if head keypoints are detected
            head_points = ['nose', 'withers', 'shoulder']  # Available keypoints
            detected_head_points = sum(1 for point in head_points if point in keypoints)
            
            # Base score on detection quality
            detection_score = detected_head_points / len(head_points)
            
            # Analyze head-neck proportions
            proportion_score = 0.5  # Default
            if 'nose' in keypoints and 'withers' in keypoints:
                # Calculate head-neck distance
                head_neck_distance = ((keypoints['nose'][0] - keypoints['withers'][0])**2 + 
                                    (keypoints['nose'][1] - keypoints['withers'][1])**2)**0.5
                # Normalize based on image size
                image_diagonal = (image.width**2 + image.height**2)**0.5
                normalized_distance = head_neck_distance / image_diagonal
                
                # Score based on typical cattle proportions
                if 0.15 <= normalized_distance <= 0.35:
                    proportion_score = 1.0
                else:
                    proportion_score = max(0.3, 1.0 - abs(normalized_distance - 0.25) * 2)
            
            score = (detection_score * 0.6) + (proportion_score * 0.4)
            return min(1.0, score)
            
        except Exception:
            return 0.5
    
    def _calculate_limb_structure_score(self, keypoints, measurements):
        """Calculate limb structure and stance score"""
        try:
            score = 0.0
            checks = 0
            
            # Check front limb alignment
            if 'shoulder' in keypoints and 'front_hoof' in keypoints:
                # Calculate vertical alignment
                x_diff = abs(keypoints['shoulder'][0] - keypoints['front_hoof'][0])
                y_diff = abs(keypoints['shoulder'][1] - keypoints['front_hoof'][1])
                
                if y_diff > 0:
                    alignment_ratio = x_diff / y_diff
                    # Good alignment should have small x difference relative to y
                    front_alignment = max(0, 1 - alignment_ratio * 0.5)
                    score += front_alignment
                    checks += 1
            
            # Check rear limb alignment
            if 'hip' in keypoints and 'rear_hoof' in keypoints:
                x_diff = abs(keypoints['hip'][0] - keypoints['rear_hoof'][0])
                y_diff = abs(keypoints['hip'][1] - keypoints['rear_hoof'][1])
                
                if y_diff > 0:
                    alignment_ratio = x_diff / y_diff
                    rear_alignment = max(0, 1 - alignment_ratio * 0.5)
                    score += rear_alignment
                    checks += 1
            
            # Check leg proportions using measurements
            if 'height_at_withers' in measurements:
                # Assume good proportions if height is reasonable
                if measurements['height_at_withers'] > 50:  # Reasonable cattle height
                    score += 0.8
                    checks += 1
            
            return score / max(1, checks)
            
        except Exception:
            return 0.6
    
    def _calculate_symmetry_score(self, keypoints):
        """Calculate overall body symmetry score"""
        try:
            score = 0.0
            checks = 0
            
            # Check body line straightness
            if 'nose' in keypoints and 'rump' in keypoints and 'withers' in keypoints:
                # Calculate body line deviation
                nose_x, nose_y = keypoints['nose']
                withers_x, withers_y = keypoints['withers']
                rump_x, rump_y = keypoints['rump']
                
                # Check if points form a reasonable line
                body_length = ((rump_x - nose_x)**2 + (rump_y - nose_y)**2)**0.5
                
                if body_length > 0:
                    # Calculate withers deviation from nose-rump line
                    line_deviation = abs((rump_y - nose_y) * withers_x - (rump_x - nose_x) * withers_y + 
                                       rump_x * nose_y - rump_y * nose_x) / body_length
                    
                    # Normalize deviation
                    normalized_deviation = line_deviation / body_length
                    symmetry_score = max(0, 1 - normalized_deviation * 5)
                    score += symmetry_score
                    checks += 1
            
            # Check stance symmetry
            if 'front_hoof' in keypoints and 'rear_hoof' in keypoints:
                front_y = keypoints['front_hoof'][1]
                rear_y = keypoints['rear_hoof'][1]
                
                # Both hooves should be at similar ground level
                y_diff = abs(front_y - rear_y)
                stance_score = max(0, 1 - y_diff / 100)  # Normalize
                score += stance_score
                checks += 1
            
            return score / max(1, checks)
            
        except Exception:
            return 0.7
    
    def _calculate_muscle_definition_score(self, image, keypoints):
        """Calculate muscle definition and body condition score"""
        try:
            # Convert image to array for analysis
            img_array = np.array(image)
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            
            # Analyze texture variance in body regions
            h, w = gray.shape
            
            # Define body region (central area)
            body_region = gray[h//4:3*h//4, w//4:3*w//4]
            
            # Calculate local variance as measure of muscle definition
            kernel_size = 15
            kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size**2)
            mean = cv2.filter2D(body_region.astype(np.float32), -1, kernel)
            sqr_mean = cv2.filter2D((body_region.astype(np.float32))**2, -1, kernel)
            variance = sqr_mean - mean**2
            
            # Calculate average variance
            avg_variance = np.mean(variance)
            
            # Normalize to 0-1 scale
            normalized_score = min(1.0, avg_variance / 500)
            
            return normalized_score
            
        except Exception:
            return 0.6
    
    def _calculate_coat_pattern_score(self, image):
        """Calculate coat pattern and color consistency score"""
        try:
            img_array = np.array(image)
            
            # Analyze color distribution uniformity
            hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
            
            # Calculate color variance in hue channel
            hue = hsv[:, :, 0]
            hue_std = np.std(hue)
            
            # Calculate saturation consistency
            saturation = hsv[:, :, 1]
            sat_std = np.std(saturation)
            
            # Combine metrics - lower variance indicates more uniform coat
            color_consistency = 1.0 / (1.0 + (hue_std + sat_std) / 100)
            
            # Also check for reasonable color distribution
            unique_colors = len(np.unique(hue))
            color_diversity = min(1.0, unique_colors / 50)
            
            # Balance consistency and natural variation
            final_score = (color_consistency * 0.7) + (color_diversity * 0.3)
            
            return min(1.0, final_score)
            
        except Exception:
            return 0.7
    
    def _generate_atc_recommendations(self, components, atc_score):
        """Generate recommendations based on ATC score components"""
        recommendations = []
        
        try:
            # Check each component and provide specific recommendations
            if components.get('body_proportions', 0) < 60:
                recommendations.append("Body proportions suggest further verification of animal type classification")
            
            if components.get('head_characteristics', 0) < 60:
                recommendations.append("Head features may benefit from better image angle or lighting")
            
            if components.get('limb_structure', 0) < 60:
                recommendations.append("Limb structure analysis suggests checking animal stance and positioning")
            
            if components.get('overall_symmetry', 0) < 60:
                recommendations.append("Image symmetry could be improved with centered animal positioning")
            
            if components.get('muscle_definition', 0) < 60:
                recommendations.append("Muscle definition analysis suggests higher resolution image may improve accuracy")
            
            if components.get('coat_pattern', 0) < 60:
                recommendations.append("Coat pattern analysis indicates possible lighting or focus improvements needed")
            
            # Overall recommendations based on ATC score
            if atc_score >= 85:
                recommendations.append("Excellent ATC score - high confidence in classification accuracy")
            elif atc_score >= 70:
                recommendations.append("Good ATC score - classification appears reliable")
            elif atc_score >= 55:
                recommendations.append("Fair ATC score - consider additional verification methods")
            else:
                recommendations.append("Low ATC score - recommend retaking image with better positioning and lighting")
            
            if not recommendations:
                recommendations.append("ATC analysis complete - all parameters within acceptable ranges")
                
        except Exception:
            recommendations = ["Error generating recommendations - using default analysis"]
        
        return recommendations