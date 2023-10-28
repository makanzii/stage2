export function friendlyTime(isoTime) {
    const now = new Date();
    const time = new Date(isoTime);

    const seconds = Math.floor((now - time) / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (seconds < 60) {
        return "just now";
    } else if (minutes < 60) {
        return `${minutes} minutes ago`;
    } else if (hours < 24) {
        return `${hours} hours ago`;
    } else if (days < 7) {
        return `${days} days ago`;
    } else if (days < 30) {
        const weeks = Math.floor(days / 7);
        return `${weeks} weeks ago`;
    } else {
        const months = Math.floor(days / 30);
        if (months < 12) {
            return `${months} months ago`;
        } else {
            const years = Math.floor(months / 12);
            return `${years} years ago`;
        }
    }
}
