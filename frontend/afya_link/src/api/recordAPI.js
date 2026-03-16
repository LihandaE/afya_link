import API from './axios';

export const getRecords =() =>
    API.get('records/');
export const createRecord =(data) =>
    API.post('records/', data);
