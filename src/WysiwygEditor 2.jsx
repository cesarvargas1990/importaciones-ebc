import ReactQuill from 'react-quill-new';
import 'react-quill-new/dist/quill.snow.css';

const allowedTags = /<(\/)?(p|h3|ul|ol|li|strong|em|br)\b[^>]*>/gi;

function sanitizeHtml(value) {
  return String(value || '')
    .replace(/<\/?(script|style)[^>]*>/gi, '')
    .replace(allowedTags, '<$1$2>');
}

const modules = {
  toolbar: [
    [{ header: [3, false] }],
    ['bold', 'italic'],
    [{ list: 'bullet' }, { list: 'ordered' }],
    ['clean'],
  ],
};

const formats = ['header', 'bold', 'italic', 'list', 'bullet', 'ordered'];

export default function WysiwygEditor({ value, onChange }) {
  return (
    <div className="wysiwyg-editor">
      <ReactQuill
        theme="snow"
        value={sanitizeHtml(value)}
        onChange={html => onChange(sanitizeHtml(html))}
        modules={modules}
        formats={formats}
        placeholder="Escribe los detalles del producto…"
      />
    </div>
  );
}
