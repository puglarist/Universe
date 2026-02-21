using UnityEngine;

namespace Universe.Video
{
    public class UniverseTubStarter : MonoBehaviour
    {
        public void RecordClip() => Debug.Log("Recording gameplay clip (implementation pending).");
        public void SaveReplay() => Debug.Log("Replay saved.");
        public void PlayReplay() => Debug.Log("Replay playing on in-game display.");
        public void Like() => Debug.Log("Liked clip.");
        public void Comment(string message) => Debug.Log($"Comment: {message}");
    }
}
