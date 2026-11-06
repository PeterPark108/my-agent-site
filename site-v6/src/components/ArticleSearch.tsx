'use client';
import { useEffect, useRef, useState } from 'react';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

const normalize = (value: string) => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/đ/g, 'd').replace(/Đ/g, 'D').toLowerCase();

/** Progressive enhancement: all checked-in articles remain readable without JS. */
export function ArticleSearch({ listId, total }: { listId: string; total: number }) {
  const [query, setQuery] = useState('');
  const [count, setCount] = useState(total);
  const input = useRef<HTMLInputElement>(null);
  function filter(value: string) {
    setQuery(value);
    const list = document.getElementById(listId);
    const cards = Array.from(list?.querySelectorAll<HTMLElement>('.news') ?? []);
    const terms = normalize(value.trim()).split(/\s+/).filter(Boolean);
    let visible = 0;
    cards.forEach(card => {
      const content = normalize(card.textContent ?? '');
      card.hidden = !terms.every(term => content.includes(term));
      if (!card.hidden) visible++;
    });
    setCount(visible);
    ScrollTrigger.refresh();
  }
  useEffect(() => () => {
    document.getElementById(listId)?.querySelectorAll<HTMLElement>('.news').forEach(card => { card.hidden = false; });
  }, [listId]);
  function clear() { filter(''); input.current?.focus(); }
  return <div className="article-search">
    <div className="article-search-row">
      <label htmlFor="article-query">Tìm bài viết trên trang này</label>
      <span className="article-result" role="status" aria-live="polite" aria-atomic="true">{`${count} bài viết${query.trim() ? ' phù hợp' : ''}`}</span>
    </div>
    <div className="article-search-field">
      <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="1.7" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 4.5 4.5"/></svg>
      <input ref={input} id="article-query" type="search" value={query} onChange={event => filter(event.target.value)} placeholder="Nhập chủ đề hoặc từ khóa…" aria-controls={listId} autoComplete="off"/>
      {query && <button type="button" onClick={clear}>Xóa tìm kiếm</button>}
    </div>
    {count === 0 && <div className="article-search-empty"><strong>Chưa tìm thấy bài phù hợp.</strong><p>Thử từ khóa ngắn hơn hoặc chọn một chủ đề khác.</p><button type="button" className="content-button ghost" onClick={clear}>Xem lại tất cả bài</button></div>}
  </div>;
}
