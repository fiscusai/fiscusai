# Owner-based Access

- Records uploads to DB table `UploadedFile` on `/files/notify-upload` with `owner_sub` from JWT (`sub`).
- `/files/download-url` requires `admin` or file owner.
- `/files/mine` lists current user's uploads.
- Frontend `/uploads` now shows your files (requires `api_token` in localStorage).