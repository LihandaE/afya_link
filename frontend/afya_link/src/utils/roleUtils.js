export const isAdmin = (user)=>{
    return user?.role === 'hospital_admin'
}

export const isDoctor= (user)=>{
    return user?.role ==='doctor'
}