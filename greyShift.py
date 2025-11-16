#!/usr/bin/env python3
"""
greyShift - Color Correction Tool
Converts images to remove color casts by analyzing tonal ranges.

This is a Python conversion of the original Processing (greyShift.pde) sketch.
"""

import argparse
import sys
import os
from PIL import Image
import numpy as np
from pathlib import Path


class GreyShift:
    """Main class for performing greyShift color correction on images."""
    
    def __init__(self, filepath, width=None, height=None, scalar=1.0):
        """
        Initialize the greyShift processor.
        
        Args:
            filepath (str): Path to the input image
            width (int): Target width for processing (optional)
            height (int): Target height for processing (optional)
            scalar (float): Correction intensity (0.0 to 1.0)
        """
        self.filepath = filepath
        self.width = width
        self.height = height
        self.scalar = scalar
        
        # Validate inputs
        self._validate_inputs()
        
        # Tonal separation variables
        self.low_count = 0
        self.mid_count = 0
        self.high_count = 0
        
        # RGB ranges for tonal analysis
        # Low tones (25% brightness range)
        self.r1, self.r2 = 54, 74
        # Mid tones (50% brightness range)  
        self.r3, self.r4 = 119, 139
        # High tones (75% brightness range)
        self.r5, self.r6 = 183, 203
        

        # Offset calculations
        self.red_low_offset = 0
        self.green_low_offset = 0
        self.blue_low_offset = 0
        
        self.red_mid_offset = 0
        self.green_mid_offset = 0
        self.blue_mid_offset = 0
        
        self.red_high_offset = 0
        self.green_high_offset = 0
        self.blue_high_offset = 0

    def _validate_inputs(self):
        """Validate input parameters."""
        if not self.filepath:
            raise ValueError("Filepath must be defined")
        
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Image file not found: {self.filepath}")
        
        if self.scalar <= 0 or self.scalar > 1:
            raise ValueError("Scalar must be greater than 0 and less than or equal to 1")

    def load_and_resize_image(self):
        """Load the image and optionally resize it."""
        try:
            self.img = Image.open(self.filepath)
            print(f"Loaded image: {self.img.size[0]}x{self.img.size[1]} pixels")
            
            # Resize if width and height are specified
            if self.width and self.height:
                self.img = self.img.resize((self.width, self.height), Image.Resampling.LANCZOS)
                print(f"Resized image to: {self.width}x{self.height} pixels")
            
            # Convert to RGB if not already
            if self.img.mode != 'RGB':
                self.img = self.img.convert('RGB')
                
        except Exception as e:
            raise Exception(f"Error loading image: {e}")

    def analyze_tonal_ranges(self):
        """Analyze pixels in different tonal ranges using vectorized operations."""
        # Convert image to numpy array for faster processing
        img_array = np.array(self.img, dtype=np.float32)
        
        print("Analyzing tonal ranges...")
        
        # Calculate average brightness for all pixels at once (vectorized)
        averages = np.mean(img_array, axis=2)
        
        # Create masks for each tonal range (vectorized boolean operations)
        low_mask = (averages >= self.r1) & (averages <= self.r2)
        mid_mask = (averages >= self.r3) & (averages <= self.r4)
        high_mask = (averages >= self.r5) & (averages <= self.r6)
        
        # Count pixels in each range
        self.low_count = np.sum(low_mask)
        self.mid_count = np.sum(mid_mask)
        self.high_count = np.sum(high_mask)
        
        # Calculate offsets using vectorized operations
        if self.low_count > 0:
            low_pixels = img_array[low_mask]
            self.red_low_offset = np.mean(low_pixels[:, 0]) - 64
            self.green_low_offset = np.mean(low_pixels[:, 1]) - 64
            self.blue_low_offset = np.mean(low_pixels[:, 2]) - 64
        else:
            self.red_low_offset = 0
            self.green_low_offset = 0
            self.blue_low_offset = 0
            
        if self.mid_count > 0:
            mid_pixels = img_array[mid_mask]
            self.red_mid_offset = np.mean(mid_pixels[:, 0]) - 129
            self.green_mid_offset = np.mean(mid_pixels[:, 1]) - 129
            self.blue_mid_offset = np.mean(mid_pixels[:, 2]) - 129
        else:
            self.red_mid_offset = 0
            self.green_mid_offset = 0
            self.blue_mid_offset = 0
            
        if self.high_count > 0:
            high_pixels = img_array[high_mask]
            self.red_high_offset = np.mean(high_pixels[:, 0]) - 193
            self.green_high_offset = np.mean(high_pixels[:, 1]) - 193
            self.blue_high_offset = np.mean(high_pixels[:, 2]) - 193
        else:
            self.red_high_offset = 0
            self.green_high_offset = 0
            self.blue_high_offset = 0
        
        # Calculate average offsets
        offsets = [
            (self.red_low_offset, self.red_mid_offset, self.red_high_offset),
            (self.green_low_offset, self.green_mid_offset,
             self.green_high_offset),
            (self.blue_low_offset, self.blue_mid_offset, self.blue_high_offset)
        ]
        self.red_avg_offset = sum(offsets[0]) / 3
        self.green_avg_offset = sum(offsets[1]) / 3
        self.blue_avg_offset = sum(offsets[2]) / 3
        
        print(f"Low-tone pixels found: {self.low_count}")
        print(f"Mid-tone pixels found: {self.mid_count}")
        print(f"High-tone pixels found: {self.high_count}")
        print(f"Low offsets: R={self.red_low_offset:.2f}, "
              f"G={self.green_low_offset:.2f}, B={self.blue_low_offset:.2f}")
        print(f"Mid offsets: R={self.red_mid_offset:.2f}, "
              f"G={self.green_mid_offset:.2f}, B={self.blue_mid_offset:.2f}")
        print(f"High offsets: R={self.red_high_offset:.2f}, "
              f"G={self.green_high_offset:.2f}, B={self.blue_high_offset:.2f}")

    def apply_correction(self):
        """Apply the greyShift correction to all pixels."""
        print("Applying greyShift correction...")
        
        # Convert image to numpy array
        img_array = np.array(self.img)
        
        # Apply corrections to each pixel using vectorized operations
        corrected_array = img_array.astype(np.float32)
        
        # Apply offsets to each channel
        corrected_array[:, :, 0] -= self.red_avg_offset * self.scalar
        corrected_array[:, :, 1] -= self.green_avg_offset * self.scalar
        corrected_array[:, :, 2] -= self.blue_avg_offset * self.scalar
        
        # Clamp values to valid range [0, 255]
        corrected_array = np.clip(np.round(corrected_array), 0, 255)
        corrected_array = corrected_array.astype(np.uint8)
        
        # Convert back to PIL Image
        self.corrected_img = Image.fromarray(corrected_array)

    def save_image(self):
        """Save the corrected image with a descriptive filename."""
        # Parse the original filepath
        path = Path(self.filepath)
        stem = path.stem  # filename without extension
        suffix = path.suffix  # file extension
        
        # Create output filename
        output_filename = f"{stem}_shifted_scalar({self.scalar}){suffix}"
        output_path = path.parent / output_filename
        
        # Preserve metadata from original image
        try:
            original_img = Image.open(self.filepath)
            # Copy EXIF and other metadata if it exists
            if hasattr(original_img, 'info') and original_img.info:
                self.corrected_img.save(output_path, **original_img.info)
            else:
                self.corrected_img.save(output_path)
        except Exception as e:
            print(f"Warning: Could not preserve metadata: {e}")
            # Fallback to saving without metadata
            self.corrected_img.save(output_path)
        
        print(f"Saved corrected image: {output_path}")
        
        return str(output_path)

    def process(self):
        """Main processing pipeline."""
        print(f"Processing image: {self.filepath}")
        print(f"Scalar: {self.scalar}")
        
        self.load_and_resize_image()
        self.analyze_tonal_ranges()
        self.apply_correction()
        output_path = self.save_image()
        
        print("Processing complete!")
        return output_path
    
    def process_with_memory_optimization(self, max_dimension=3280):
        """Process with memory optimization: analyze resized, apply to original.
        
        Args:
            max_dimension (int): Maximum dimension for analysis (default 3280px)
        
        Returns:
            str: Path to the processed full-resolution image
        """
        print(f"Processing image with memory optimization: {self.filepath}")
        print(f"Max dimension for analysis: {max_dimension}px")
        print(f"Scalar: {self.scalar}")
        
        # First, check original dimensions without loading full image
        with Image.open(self.filepath) as img_check:
            original_width, original_height = img_check.size
            print(f"Original image: {original_width}x{original_height} pixels")
        
        # Check if resizing is needed for analysis
        max_original_dimension = max(original_width, original_height)
        
        if max_original_dimension > max_dimension:
            # STEP 1: Analyze resized version (memory-efficient)
            scale_factor = max_dimension / max_original_dimension
            analysis_width = int(original_width * scale_factor)
            analysis_height = int(original_height * scale_factor)
            
            print(f"Resizing for analysis: {analysis_width}x{analysis_height}")
            
            # Load and resize for analysis only
            with Image.open(self.filepath) as original_img:
                if original_img.mode != 'RGB':
                    original_img = original_img.convert('RGB')
                analysis_img = original_img.resize(
                    (analysis_width, analysis_height), 
                    Image.Resampling.LANCZOS
                )
            
            # Analyze the resized version
            self.img = analysis_img
            self.analyze_tonal_ranges()
            
            # Free memory
            del analysis_img
            del self.img
            
            # STEP 2: Apply correction to original (load fresh)
            print(f"Applying correction to original {original_width}x{original_height}")
            with Image.open(self.filepath) as original_img:
                if original_img.mode != 'RGB':
                    original_img = original_img.convert('RGB')
                self.img = original_img
                self.apply_correction()
                output_path = self.save_image()
            
        else:
            # Image is small enough, process normally
            print("Image within size limit, processing at full resolution")
            self.load_and_resize_image()
            self.analyze_tonal_ranges()
            self.apply_correction()
            output_path = self.save_image()
        
        print("Processing complete!")
        return output_path


def main():
    """Main entry point for command-line usage."""
    parser = argparse.ArgumentParser(
        description="greyShift - Remove color casts from images",
        epilog="Example: python greyshift.py --filepath image.jpg --scalar 0.8"
    )
    
    parser.add_argument(
        '--filepath',
        required=True,
        help='Path to the input image file'
    )
    
    parser.add_argument(
        '--w', '--width',
        type=int,
        help='Target width for processing (optional)'
    )
    
    parser.add_argument(
        '--h', '--height',
        type=int,
        help='Target height for processing (optional)'
    )
    
    parser.add_argument(
        '--scalar',
        type=float,
        default=1.0,
        help='Correction intensity (0.0 to 1.0, default: 1.0)'
    )
    
    args = parser.parse_args()
    
    try:
        # Create and run the greyShift processor
        processor = GreyShift(
            filepath=args.filepath,
            width=args.w,
            height=args.h,
            scalar=args.scalar
        )
        
        output_path = processor.process()
        print(f"\n✅ Success! Corrected image saved to: {output_path}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
