export function onlyFields(input:Record<string,unknown>,fields:string[]){if(Object.keys(input).some(k=>!fields.includes(k)))throw new Error('Trường dữ liệu không hợp lệ.');}
