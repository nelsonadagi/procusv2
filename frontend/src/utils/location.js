export const detectUserLocation = () => {
    return new Promise((resolve, reject) => {
        if (!navigator.geolocation) {
            reject(new Error('Geolocation not supported'));
        } else {
            navigator.geolocation.getCurrentPosition((position) => {
                const loc = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };
                localStorage.setItem('user_location', JSON.stringify(loc));
                resolve(loc);
            }, (error) => {
                reject(error);
            }, {
                enableHighAccuracy: true,
                timeout: 5000,
                maximumAge: 0
            });
        }
    });
};

export const getStoredLocation = () => {
    const loc = localStorage.getItem('user_location');
    return loc ? JSON.parse(loc) : null;
};
