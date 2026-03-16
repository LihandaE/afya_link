import {Link} from 'react-router-dom';

export default function Sidebar(){
    return(
        <div>
            <Link to='/dashboard'>Dashboard</Link> <br />
            <Link to='/patients'>Patients</Link><br />
            <Link to='/doctors'>Doctors</Link>
        </div>
    );
}