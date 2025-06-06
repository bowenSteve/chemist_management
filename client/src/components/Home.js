import { useState, useEffect } from "react";

function Home() {
  const [medicines, setMedicines] = useState([]);
  const [stats, setStats] = useState({});
  const [categories, setCategories] = useState([]);
  const [manufacturers, setManufacturers] = useState([]);
  const [selectedOption, setSelectedOption] = useState('All');
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch medicines data
    fetch('http://localhost:5000/api/medicines')
      .then(res => res.json())
      .then(data => {
        setMedicines(data.medicines || []);
        console.log('Medicines:', data);
      })
      .catch(error => {
        console.error('Error fetching medicines:', error);
        setError('Failed to load medicines');
      });

    // Fetch statistics
    fetch('http://localhost:5000/api/stats')
      .then(res => res.json())
      .then(data => {
        setStats(data);
        console.log('Stats:', data);
      })
      .catch(error => {
        console.error('Error fetching stats:', error);
      });

    // Fetch categories
    fetch('http://localhost:5000/api/categories')
      .then(res => res.json())
      .then(data => {
        setCategories(data.categories || []);
        console.log('Categories:', data);
      })
      .catch(error => {
        console.error('Error fetching categories:', error);
      });

    // Fetch manufacturers
    fetch('http://localhost:5000/api/manufacturers')
      .then(res => res.json())
      .then(data => {
        setManufacturers(data.manufacturers || []);
        console.log('Manufacturers:', data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching manufacturers:', error);
        setLoading(false);
      });
  }, []);

  function handleSelect(eventKey) {
    setSelectedOption(eventKey);
  }

  function handleSearch(event) {
    setSearchTerm(event.target.value);
  }

  function handleMedicineClick(id) {
    // navigate(`/medicine/${id}`);
    console.log('Medicine clicked:', id);
  }

  // Filter medicines based on search term and selected category
  const filteredMedicines = medicines.filter(medicine => {
    const matchesSearch = medicine.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         medicine.manufacturer.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         medicine.category.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesCategory = selectedOption === 'All' || medicine.category === selectedOption;
    
    return matchesSearch && matchesCategory;
  });

  // Get status badge color and text
  function getStatusBadge(medicine) {
    if (medicine.quantity <= 10) {
      return { color: 'bg-danger', text: 'Low Stock' };
    } else if (medicine.quantity <= 50) {
      return { color: 'bg-warning', text: 'Medium Stock' };
    } else {
      return { color: 'bg-success', text: 'In Stock' };
    }
  }

  if (loading) {
    return (
      <div>
        {/* <Navbar /> */}
        <div className="container mt-4">
          <div className="text-center">
            <div className="spinner-border" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
            <p className="mt-2">Loading medicines...</p>
          </div>
        </div>
        {/* <Footer /> */}
      </div>
    );
  }

  return (
    <div>
      {/* <Navbar /> */}
      
      {/* Hero Image */}
      <header>
        <img
          src="https://via.placeholder.com/1200x400/4A90E2/FFFFFF?text=Pharmacy+Management+System"
          alt="Pharmacy Management"
          className="img-fluid w-100"
          style={{ width: '100%', height: '50vh', objectFit: 'cover' }}
        />
      </header>

      <main className="container mt-4">
        {/* Statistics Cards */}
        <div className="row mb-4">
          <div className="col-md-3 mb-3">
            <div className="card text-center bg-primary text-white">
              <div className="card-body">
                <h5 className="card-title">Total Medicines</h5>
                <h2 className="card-text">{stats.total_medicines || 0}</h2>
              </div>
            </div>
          </div>
          <div className="col-md-3 mb-3">
            <div className="card text-center bg-info text-white">
              <div className="card-body">
                <h5 className="card-title">Categories</h5>
                <h2 className="card-text">{stats.total_categories || 0}</h2>
              </div>
            </div>
          </div>
          <div className="col-md-3 mb-3">
            <div className="card text-center bg-success text-white">
              <div className="card-body">
                <h5 className="card-title">Manufacturers</h5>
                <h2 className="card-text">{stats.total_manufacturers || 0}</h2>
              </div>
            </div>
          </div>
          <div className="col-md-3 mb-3">
            <div className="card text-center bg-warning text-white">
              <div className="card-body">
                <h5 className="card-title">Low Stock Items</h5>
                <h2 className="card-text">{stats.low_stock_items || 0}</h2>
              </div>
            </div>
          </div>
        </div>

        <h1 className="main mt-2 text-center">MEDICINE INVENTORY</h1>
        
        {error && (
          <div className="alert alert-danger" role="alert">
            {error}
          </div>
        )}

        {/* Filter and Search Controls */}
        <div className="d-flex justify-content-between align-items-center flex-wrap mb-4">
          <div className="dropdown mb-2">
            <button 
              className="btn btn-primary dropdown-toggle" 
              type="button" 
              id="dropdownMenuButton" 
              data-bs-toggle="dropdown" 
              aria-expanded="false"
            >
              {selectedOption}
            </button>
            <ul className="dropdown-menu" aria-labelledby="dropdownMenuButton">
              <li>
                <a className="dropdown-item" href="#" onClick={() => handleSelect('All')}>
                  All Categories
                </a>
              </li>
              {categories.map((category, index) => (
                <li key={index}>
                  <a 
                    className="dropdown-item" 
                    href="#" 
                    onClick={() => handleSelect(category.name)}
                  >
                    {category.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>
          
          <div className="search-wrapper mb-2">
            <input
              type="text"
              className="form-control"
              placeholder="Search medicine, manufacturer, or category..."
              value={searchTerm}
              onChange={handleSearch}
              style={{ minWidth: '300px' }}
            />
          </div>
        </div>

        {/* Medicines Grid */}
        <div className="row">
          {filteredMedicines.length === 0 ? (
            <div className="col-12 text-center">
              <p className="text-muted">No medicines found matching your search criteria.</p>
            </div>
          ) : (
            filteredMedicines.map((medicine, index) => {
              const statusBadge = getStatusBadge(medicine);
              return (
                <div 
                  key={index} 
                  className="col-lg-4 col-md-6 mb-4" 
                  onClick={() => handleMedicineClick(medicine.id)}
                  style={{ cursor: 'pointer' }}
                >
                  <div className="card h-100 shadow-sm hover-shadow">
                    <div className="card-header d-flex justify-content-between align-items-center">
                      <h5 className="card-title mb-0">{medicine.name}</h5>
                      <span className={`badge ${statusBadge.color}`}>
                        {statusBadge.text}
                      </span>
                    </div>
                    <div className="card-body">
                      <p className="card-text">
                        <strong>Batch:</strong> {medicine.batch_number}
                      </p>
                      <p className="card-text">
                        <strong>Price:</strong> ₹{parseFloat(medicine.price).toFixed(2)}
                      </p>
                      <p className="card-text">
                        <strong>Quantity:</strong> {medicine.quantity} units
                      </p>
                      <p className="card-text">
                        <strong>Category:</strong> {medicine.category}
                      </p>
                      <p className="card-text">
                        <strong>Manufacturer:</strong> {medicine.manufacturer}
                      </p>
                      <div className="mt-3">
                        <small className="text-muted">
                          Added: {new Date(medicine.created_at).toLocaleDateString()}
                        </small>
                      </div>
                    </div>
                    <div className="card-footer">
                      <div className="d-flex justify-content-between">
                        <button className="btn btn-sm btn-outline-primary">
                          View Details
                        </button>
                        <button className="btn btn-sm btn-outline-secondary">
                          Edit
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Quick Actions */}
        <div className="row mt-5 mb-4">
          <div className="col-12">
            <div className="card">
              <div className="card-header">
                <h5>Quick Actions</h5>
              </div>
              <div className="card-body">
                <div className="row">
                  <div className="col-md-3 mb-2">
                    <button 
                      className="btn btn-success w-100"
                      onClick={() => console.log('Add medicine clicked')}
                    >
                      Add New Medicine
                    </button>
                  </div>
                  <div className="col-md-3 mb-2">
                    <button 
                      className="btn btn-info w-100"
                      onClick={() => console.log('Categories clicked')}
                    >
                      Manage Categories
                    </button>
                  </div>
                  <div className="col-md-3 mb-2">
                    <button 
                      className="btn btn-warning w-100"
                      onClick={() => console.log('Low stock clicked')}
                    >
                      Low Stock Report
                    </button>
                  </div>
                  <div className="col-md-3 mb-2">
                    <button 
                      className="btn btn-secondary w-100"
                      onClick={() => console.log('Manufacturers clicked')}
                    >
                      Manage Manufacturers
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
      
      {/* <Footer /> */}
    </div>
  );
}

export default Home;