import ReactQuill from 'react-quill-new';
import Quill from 'quill';
import QuillTableBetter from 'quill-table-better';
import 'react-quill-new/dist/quill.snow.css';
import 'quill-table-better/dist/quill-table-better.css';

Quill.register({ 'modules/table-better': QuillTableBetter }, true);

const allowedTags = new Set([
  'p', 'h2', 'h3', 'ul', 'ol', 'li', 'strong', 'em', 'u', 's', 'br',
  'a', 'img', 'blockquote', 'table', 'thead', 'tbody', 'tfoot', 'tr', 'th', 'td',
]);

const allowedAttributes = {
  a: new Set(['href', 'target', 'rel']),
  img: new Set(['src', 'alt', 'width', 'height']),
  th: new Set(['colspan', 'rowspan']),
  td: new Set(['colspan', 'rowspan']),
};

function isSafeUrl(value, allowDataImage = false) {
  try {
    const url = new URL(value, window.location.origin);
    return ['http:', 'https:', 'mailto:'].includes(url.protocol)
      || (allowDataImage && url.protocol === 'data:' && url.pathname.startsWith('image/'));
  } catch {
    return false;
  }
}

export function sanitizeHtml(value) {
  if (typeof window === 'undefined') return String(value || '');
  const parser = new DOMParser();
  const documentFragment = parser.parseFromString(String(value || ''), 'text/html');
  documentFragment.querySelectorAll('script,style,iframe,object,embed,form,input,button,meta,link').forEach(node => node.remove());

  documentFragment.body.querySelectorAll('thead, tfoot').forEach(section => {
    const table = section.closest('table');
    const body = table?.querySelector('tbody') || table?.appendChild(documentFragment.createElement('tbody'));
    Array.from(section.querySelectorAll('tr')).forEach(row => body.appendChild(row));
    section.remove();
  });
  documentFragment.body.querySelectorAll('th').forEach(cell => {
    const replacement = documentFragment.createElement('td');
    replacement.innerHTML = cell.innerHTML;
    ['colspan', 'rowspan'].forEach(attribute => {
      if (cell.hasAttribute(attribute)) replacement.setAttribute(attribute, cell.getAttribute(attribute));
    });
    cell.replaceWith(replacement);
  });

  documentFragment.body.querySelectorAll('*').forEach(node => {
    const tag = node.tagName.toLowerCase();
    if (!allowedTags.has(tag)) {
      node.replaceWith(...Array.from(node.childNodes));
      return;
    }
    Array.from(node.attributes).forEach(attribute => {
      const name = attribute.name.toLowerCase();
      const allowed = allowedAttributes[tag]?.has(name);
      if (!allowed || (name === 'href' && !isSafeUrl(attribute.value)) || (name === 'src' && !isSafeUrl(attribute.value, true))) {
        node.removeAttribute(attribute.name);
      }
    });
    if (tag === 'a' && node.getAttribute('href')) {
      node.setAttribute('target', '_blank');
      node.setAttribute('rel', 'noopener noreferrer');
    }
  });
  return documentFragment.body.innerHTML;
}

const modules = {
  table: false,
  toolbar: [
    [{ header: [2, 3, false] }],
    ['bold', 'italic', 'underline', 'strike'],
    [{ list: 'bullet' }, { list: 'ordered' }],
    ['link', 'image', 'table-better'],
    ['clean'],
  ],
  'table-better': {
    language: 'en_US',
    menus: ['column', 'row', 'merge', 'table', 'cell', 'wrap', 'delete'],
    toolbarTable: true,
  },
  keyboard: { bindings: QuillTableBetter.keyboardBindings },
};

const formats = [
  'header', 'bold', 'italic', 'underline', 'strike', 'list', 'bullet', 'ordered',
  'link', 'image', 'table', 'table-better', 'colspan', 'rowspan',
];

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
