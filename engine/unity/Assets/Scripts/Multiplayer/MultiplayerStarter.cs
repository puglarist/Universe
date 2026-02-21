using UnityEngine;

namespace Universe.Multiplayer
{
    public class MultiplayerStarter : MonoBehaviour
    {
        [Range(1, 4)] public int maxPartySize = 4;

        public void OpenLobby() => Debug.Log("Lobby opened (network backend pending).");
        public void SendFriendInvite(string playerId) => Debug.Log($"Invite sent to {playerId}");
        public void StartVoiceChat() => Debug.Log("Voice chat initialized (transport pending).");
    }
}
