import { useState, useRef } from 'react';
import { Upload, FileText, Loader2, CheckCircle, AlertCircle, X } from 'lucide-react';
import { useMutation } from '@tanstack/react-query';
import fileUploadService from '../services/fileUpload';
import type { Publication } from '../types';

interface FileUploaderProps {
  onPublicationsLoaded: (publications: Publication[]) => void;
  acceptedFormats?: string[];
  maxSizeMB?: number;
  buttonText?: string;
  buttonClassName?: string;
}

export default function FileUploader({
  onPublicationsLoaded,
  acceptedFormats = ['.json', '.bib', '.bibtex', '.ris', '.csv'],
  maxSizeMB = 10,
  buttonText = 'Cargar archivo',
  buttonClassName = 'bg-green-600 text-white hover:bg-green-700',
}: FileUploaderProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [error, setError] = useState<string>('');
  const [success, setSuccess] = useState<string>('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const uploadMutation = useMutation({
    mutationFn: (file: File) => fileUploadService.parseFile(file),
    onSuccess: (data) => {
      setSuccess(`✓ ${data.total_publications} publicaciones cargadas desde ${data.filename}`);
      setError('');
      onPublicationsLoaded(data.publications);
      setSelectedFile(null);
      // Limpiar mensaje después de 5 segundos
      setTimeout(() => setSuccess(''), 5000);
    },
    onError: (err: Error | { response?: { data?: { detail?: string } } }) => {
      const errorMessage = 
        (err as { response?: { data?: { detail?: string } } }).response?.data?.detail || 
        'Error al cargar el archivo';
      setError(errorMessage);
      setSuccess('');
    },
  });

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setError('');
    setSuccess('');

    // Validar tipo de archivo
    const typeValidation = fileUploadService.validateFileType(file);
    if (!typeValidation.valid) {
      setError(typeValidation.error!);
      return;
    }

    // Validar tamaño
    const sizeValidation = fileUploadService.validateFileSize(file, maxSizeMB);
    if (!sizeValidation.valid) {
      setError(sizeValidation.error!);
      return;
    }

    setSelectedFile(file);
  };

  const handleUpload = () => {
    if (selectedFile) {
      uploadMutation.mutate(selectedFile);
    }
  };

  const handleCancel = () => {
    setSelectedFile(null);
    setError('');
    setSuccess('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="space-y-3">
      {/* Botón principal */}
      <div className="flex gap-2">
        <button
          type="button"
          onClick={handleButtonClick}
          disabled={uploadMutation.isPending}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed ${buttonClassName}`}
        >
          <Upload className="w-4 h-4" />
          {buttonText}
        </button>
        
        <input
          ref={fileInputRef}
          type="file"
          accept={acceptedFormats.join(',')}
          onChange={handleFileSelect}
          className="hidden"
        />
      </div>

      {/* Archivo seleccionado */}
      {selectedFile && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <FileText className="w-5 h-5 text-blue-600" />
              <div>
                <p className="text-sm font-medium text-gray-900">{selectedFile.name}</p>
                <p className="text-xs text-gray-600">
                  {(selectedFile.size / 1024).toFixed(2)} KB
                </p>
              </div>
            </div>
            <div className="flex gap-2">
              <button
                onClick={handleUpload}
                disabled={uploadMutation.isPending}
                className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-300 flex items-center gap-1"
              >
                {uploadMutation.isPending ? (
                  <>
                    <Loader2 className="w-3 h-3 animate-spin" />
                    Procesando...
                  </>
                ) : (
                  'Cargar'
                )}
              </button>
              <button
                onClick={handleCancel}
                disabled={uploadMutation.isPending}
                className="px-3 py-1 text-sm bg-gray-200 text-gray-700 rounded hover:bg-gray-300 disabled:bg-gray-100"
              >
                <X className="w-3 h-3" />
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Mensaje de éxito */}
      {success && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-3 flex items-start gap-2">
          <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
          <p className="text-sm text-green-800">{success}</p>
        </div>
      )}

      {/* Mensaje de error */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-3 flex items-start gap-2">
          <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      {/* Info de formatos aceptados */}
      {!selectedFile && !success && (
        <p className="text-xs text-gray-500">
          Formatos: {acceptedFormats.join(', ')} | Máximo: {maxSizeMB}MB
        </p>
      )}
    </div>
  );
}
