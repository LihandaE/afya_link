import {getToken} from '../utils/tokenService';

export const useAuth = ()=>{
    const token = getToken();
    return {isAuthenticated: !!token};
};