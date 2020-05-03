import React from 'react'
import ReactLoading from 'react-loading';
import {post} from 'axios';

class SimpleReactFileUpload extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            file: null,
            content: "",
            isLoading: false,
            timer: 300
        }
        this.onFormSubmit = this.onFormSubmit.bind(this)
        this.onChange = this.onChange.bind(this)
        this.fileUpload = this.fileUpload.bind(this)
    }

    onFormSubmit(e) {
        e.preventDefault()
        this.setState({isLoading: true})// Stop form submit
        this.fileUpload(this.state.file).then((response) => {
            this.setState({content: response.data})
        })
    }

    onChange(e) {
        this.setState({file: e.target.files[0]})
    }

    fileUpload(file) {
        const url = 'http://0.0.0.0:5000/send_audio_file';
        const formData = new FormData();
        formData.append('file', file)
        const config = {
            headers: {
                'content-type': 'multipart/form-data'
            }
        }
        return post(url, formData, config)
    }

    render() {
        const {isLoading, content} = this.state
        return (
            <>
                <form onSubmit={this.onFormSubmit}>
                    <h1>File Upload</h1>
                    <input type="file" onChange={this.onChange}/>
                    <button type="submit">Upload</button>

                </form>
                <hr/>
                {isLoading && !content &&
                    <div>
                        <ReactLoading type={"balls"} color={"#a4a4a4"} height={'10%'} width={'10%'}/>,
                        <h3>O Tempo de conversão e equivalente ao tempo de duração do audio</h3>
                    </div>
                }
                {content &&
                <span>{content['content']}</span>
                }
            </>
        )
    }
}

export default SimpleReactFileUpload
