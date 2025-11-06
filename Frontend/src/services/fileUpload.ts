/**
 * Servicio para carga y parseo de archivos bibliográficos
 * 
 * Soporta: JSON, BibTeX, RIS, CSV
 */

import api from './api';
import type { Publication } from '../types';

export interface FileUploadResponse {
  success: boolean;
  filename: string;
  format: string;
  total_publications: number;
  publications: Publication[];
}

class FileUploadService {
  /**
   * Sube y parsea un archivo bibliográfico
   */
  async parseFile(file: File): Promise<FileUploadResponse> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post<FileUploadResponse>('/api/v1/upload/parse', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  }

  /**
   * Valida que el archivo tenga una extensión soportada
   */
  validateFileType(file: File): { valid: boolean; error?: string } {
    const validExtensions = ['.json', '.bib', '.bibtex', '.ris', '.csv'];
    const fileName = file.name.toLowerCase();
    const isValid = validExtensions.some(ext => fileName.endsWith(ext));

    if (!isValid) {
      return {
        valid: false,
        error: `Formato no soportado. Use: ${validExtensions.join(', ')}`,
      };
    }

    return { valid: true };
  }

  /**
   * Valida el tamaño del archivo (máximo 10MB)
   */
  validateFileSize(file: File, maxSizeMB: number = 10): { valid: boolean; error?: string } {
    const maxSizeBytes = maxSizeMB * 1024 * 1024;
    
    if (file.size > maxSizeBytes) {
      return {
        valid: false,
        error: `El archivo es demasiado grande. Máximo: ${maxSizeMB}MB`,
      };
    }

    return { valid: true };
  }
}

export default new FileUploadService();
