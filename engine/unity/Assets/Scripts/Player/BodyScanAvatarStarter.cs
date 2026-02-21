using UnityEngine;

namespace Universe.Player
{
    public class BodyScanAvatarStarter : MonoBehaviour
    {
        public Renderer faceRenderer;
        public Texture2D faceTexture;

        public void ImportPhoto(Texture2D photo)
        {
            faceTexture = photo;
            Debug.Log("Photo imported for avatar reference.");
        }

        public void ApplyFaceTexture()
        {
            if (faceRenderer != null && faceTexture != null)
                faceRenderer.material.mainTexture = faceTexture;
        }
    }
}
