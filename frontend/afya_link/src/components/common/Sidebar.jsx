import {Link} from 'react-router-dom';

export default function Sidebar(){
    return(
        <div style={{width: '200px', height: '100%', background: '#f0f0f0', padding: '10px'}}>
            <Link to='/dashboard'>Dashboard</Link> <br />
            <Link to='/patients'>Patients</Link><br />
            <Link to='/doctors'>Doctors</Link>
        </div>
    );
}