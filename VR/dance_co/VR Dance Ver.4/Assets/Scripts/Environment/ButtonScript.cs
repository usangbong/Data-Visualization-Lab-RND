using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ButtonScript : MonoBehaviour
{
    public GameObject obj;
    SavePos spt;

    void Start()
    {
        spt = obj.GetComponent<SavePos>();
    }

    public void OnClick()
    {
        spt.setButton(true);
    }

    public void Quit()
    {
        UnityEditor.EditorApplication.isPlaying = false;
    }
}
