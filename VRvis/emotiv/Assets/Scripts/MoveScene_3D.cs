using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class MoveScene_3D : MonoBehaviour
{
    private void Awake()
    {
        DontDestroyOnLoad(this.gameObject);
    }
    // Update is called once per frame
    void Update()
    {

        int idx = SceneManager.GetActiveScene().buildIndex;

        if (Input.GetKeyDown(KeyCode.RightArrow))
        {
            if (idx + 1 <= 14)
                SceneManager.LoadScene(idx + 1);
        }

        else if (Input.GetKeyDown(KeyCode.LeftArrow))
        {
            if (idx - 1 >= 8)
                SceneManager.LoadScene(idx - 1);
        }

    }
}
